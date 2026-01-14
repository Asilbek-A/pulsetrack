# BLE Ma'lumotlar O'qish va Tahlil Qilish - Batafsil Tushuntirish

## 📡 1. BLE Ulanish Jarayoni

### 1.1. Qurilma Skanni Qilish
```dart
// whoop_app/lib/core/services/ble_health_service.dart
Future<List<ScanResult>> scanDevices()
```
- Bluetooth Low Energy orqali qurilmalarni qidiradi
- **Service UUID'lari** asosida filtrlash:
  - `0000180d` - Heart Rate Service (standart)
  - `0000fee0` - Huawei/Xiaomi specific
  - `00001822` - SpO2 Service
  - `00001809` - Temperature Service

### 1.2. Qurilma Ulanish
```dart
Future<bool> connectToDevice(BluetoothDevice device)
```
1. **Connect** - BluetoothDevice.connect()
2. **Discover Services** - device.discoverServices()
3. **Subscribe to Characteristics** - setNotifyValue(true)
4. **Read Device Info** - manufacturer, model, firmware

---

## 🔍 2. Ma'lumotlar O'qish (Data Reading)

### 2.1. BLE Services va Characteristics

#### **Heart Rate Service** (`0000180d`)
- **Characteristic**: `00002a37` (Heart Rate Measurement)
- **Ma'lumotlar**:
  - Heart Rate (BPM) - 8-bit yoki 16-bit
  - R-R Interval (HRV uchun) - millisekundlarda
  - Energy Expended (kaloriya)

**Qanday o'qiladi:**
```dart
// ble_health_service.dart:309
await char.setNotifyValue(true); // Notification yoqiladi
_hrSubscription = char.onValueReceived.listen((value) {
  _parseHeartRateData(Uint8List.fromList(value));
});
```

#### **SpO2 Service** (`00001822`)
- **Characteristic**: `00002a5f` (PLX Continuous Measurement)
- **Ma'lumotlar**:
  - SpO2 foizi (0-100%)
  - Perfusion Index

#### **Temperature Service** (`00001809`)
- **Characteristic**: `00002a1c` (Temperature Measurement)
- **Ma'lumotlar**:
  - Harorat (Celsius) - IEEE 11073 formatida

#### **Huawei/Xiaomi Specific Services**
- **Service**: `0000fee0` / `0000fee1`
- **Characteristics**:
  - `00000007` - Steps (qadamlar)
  - `00000008` - Activity (faollik)
  - `00000009` - Sleep (uyqu)

---

## 📊 3. Ma'lumotlarni Parse Qilish (Parsing)

### 3.1. Heart Rate Parse
```dart
// ble_health_service.dart:483
void _parseHeartRateData(Uint8List data) {
  int flags = data[0];
  bool isFormat16Bit = (flags & 0x01) != 0;
  bool hasRRInterval = (flags & 0x10) != 0;
  
  // Heart Rate o'qish
  int heartRate = isFormat16Bit 
    ? data[1] | (data[2] << 8)  // 16-bit
    : data[1];                   // 8-bit
  
  // R-R Interval o'qish (HRV uchun)
  if (hasRRInterval) {
    int rrRaw = data[offset] | (data[offset + 1] << 8);
    int rrInterval = (rrRaw * 1000 ~/ 1024); // millisekundga o'tkazish
    
    // HRV hisoblash uchun saqlash
    _rrIntervals.add(rrInterval);
  }
}
```

**Ma'lumotlar format:**
```
Byte 0: Flags (bit mask)
  Bit 0: 0 = 8-bit HR, 1 = 16-bit HR
  Bit 4: 1 = R-R interval bor
Byte 1-2: Heart Rate (BPM)
Byte 3-4: R-R Interval (optional)
```

### 3.2. SpO2 Parse
```dart
// ble_health_service.dart:547
void _parseSpO2Data(Uint8List data) {
  int spo2 = data[1];  // SpO2 foizi
  int? perfusionIndex = data.length > 3 ? data[3] : null;
}
```

### 3.3. Temperature Parse
```dart
// ble_health_service.dart:570
void _parseTemperatureData(Uint8List data) {
  // IEEE 11073 FLOAT format
  int mantissa = data[1] | (data[2] << 8) | ((data[3] & 0x0F) << 16);
  int exponent = (data[3] >> 4) & 0x0F;
  double celsius = mantissa * pow(10, exponent);
}
```

### 3.4. Steps Parse (Huawei/Xiaomi)
```dart
// ble_health_service.dart:596
void _parseHuaweiData(String charUuid, Uint8List data) {
  if (data.length >= 4) {
    int steps = data[0] | (data[1] << 8) | (data[2] << 16) | (data[3] << 24);
    _todaySteps = steps;
    _todayDistance = steps * 0.75; // ~0.75m per step
  }
}
```

---

## 🧮 4. Metrikalarni Hisoblash (Algorithms)

### 4.1. HRV (Heart Rate Variability) Hisoblash
```dart
// ble_health_service.dart:700+
HRVReading calculateHRV() {
  if (_rrIntervals.length < 10) return null;
  
  // RMSSD - Root Mean Square of Successive Differences
  double sumSquaredDiffs = 0;
  for (int i = 1; i < _rrIntervals.length; i++) {
    double diff = _rrIntervals[i] - _rrIntervals[i-1];
    sumSquaredDiffs += diff * diff;
  }
  double rmssd = sqrt(sumSquaredDiffs / (_rrIntervals.length - 1));
  
  // pNN50 - Percentage of intervals differing by >50ms
  int nn50 = 0;
  for (int i = 1; i < _rrIntervals.length; i++) {
    if ((_rrIntervals[i] - _rrIntervals[i-1]).abs() > 50) {
      nn50++;
    }
  }
  double pnn50 = (nn50 / (_rrIntervals.length - 1)) * 100;
  
  return HRVReading(rmssd: rmssd, pnn50: pnn50);
}
```

**HRV nima?**
- R-R interval'lar orasidagi o'zgarish
- Yuqori HRV = yaxshi recovery, past stress
- Past HRV = charchoq, stress

### 4.2. Recovery Score Hisoblash
```dart
// health_algorithm_service.dart:123
int calculateRecoveryScore({
  SleepSession? lastNightSleep,
  double? previousDayStrain,
}) {
  double score = 50; // Base score
  
  // HRV component (35%)
  HRVReading? hrv = _bleService.calculateHRV();
  if (hrv != null) {
    double hrvRatio = hrv.rmssd / _userProfile.baselineHRV;
    double hrvScore = 50 + (hrvRatio - 1) * 50;
    score = score * 0.65 + hrvScore * 0.35;
  }
  
  // Resting HR component (25%)
  int? restingHR = _bleService.getRestingHR();
  if (restingHR != null) {
    double hrRatio = _userProfile.restingHR / restingHR;
    double hrScore = 50 + (hrRatio - 1) * 100;
    score = score * 0.75 + hrScore * 0.25;
  }
  
  // Sleep component (25%)
  if (lastNightSleep != null) {
    score = score * 0.75 + lastNightSleep.sleepScore * 0.25;
  }
  
  // Previous day strain penalty (15%)
  if (previousDayStrain != null && previousDayStrain > 15) {
    double strainPenalty = (previousDayStrain - 15) * 3;
    score -= strainPenalty;
  }
  
  return score.round().clamp(0, 100);
}
```

**Recovery Score Formula:**
```
Recovery = (HRV × 35%) + (RestingHR × 25%) + (Sleep × 25%) - (Strain Penalty × 15%)
```

### 4.3. Strain Score Hisoblash
```dart
// health_algorithm_service.dart:172
double calculateStrainScore() {
  return (_todayStrain / 100).clamp(0.0, 21.0);
}

double _calculateStrainContribution(HeartRateZone zone) {
  switch (zone) {
    case HeartRateZone.rest:      return 0.0;
    case HeartRateZone.warmup:     return 0.02;
    case HeartRateZone.fatBurn:    return 0.08;
    case HeartRateZone.cardio:     return 0.25;
    case HeartRateZone.peak:       return 0.70;
    case HeartRateZone.maxEffort:  return 1.50;
  }
}
```

**Strain Score:**
- Har bir HR reading uchun zone bo'yicha strain qo'shiladi
- 0.0 - 21.0 oralig'ida
- Yuqori HR zone = ko'proq strain

### 4.4. Sleep Stages Aniqlash
```dart
// health_algorithm_service.dart:355
List<SleepStage> _detectSleepStages(List<HeartRateReading> hrReadings, DateTime startTime) {
  // 5 daqiqalik oynalar (windows)
  for (int i = 0; i < hrReadings.length; i += 5) {
    var window = hrReadings.sublist(i, i + 5);
    double windowAvgHR = window.map((r) => r.bpm).reduce((a, b) => a + b) / window.length;
    double hrVariability = calculateVariability(window);
    
    SleepStageType detectedStage;
    
    if (windowAvgHR > avgHR + 10 || hrVariability > 8) {
      detectedStage = SleepStageType.awake;  // Yuqori HR yoki o'zgaruvchan
    } else if (hrRatio < 0.92 && hrVariability < 3) {
      detectedStage = SleepStageType.deep;   // Past HR, past o'zgaruvchanlik
    } else if (hrRatio > 0.98 && hrVariability > 4) {
      detectedStage = SleepStageType.rem;    // O'rtacha HR, yuqori o'zgaruvchanlik
    } else {
      detectedStage = SleepStageType.light;   // Qolgan hollar
    }
  }
}
```

**Sleep Stages:**
- **Awake**: HR > baseline + 10, yuqori variability
- **Light**: O'rtacha HR, o'rtacha variability
- **Deep**: HR < baseline - 8%, past variability
- **REM**: HR ≈ baseline, yuqori variability

### 4.5. Stress Level Hisoblash
```dart
// health_algorithm_service.dart:487
int calculateStressLevel() {
  double stressScore = 50; // baseline
  
  // HRV-based stress (past HRV = yuqori stress)
  HRVReading? hrv = _bleService.calculateHRV();
  if (hrv != null) {
    double hrvRatio = hrv.rmssd / _userProfile.baselineHRV;
    if (hrvRatio < 0.7) stressScore += 30;  // Yuqori stress
    else if (hrvRatio < 0.9) stressScore += 15;  // O'rtacha stress
    else if (hrvRatio > 1.1) stressScore -= 15;  // Past stress
  }
  
  // Current HR vs resting (yuqori HR = stress)
  if (currentHR > restingHR * 1.3) stressScore += 20;
  
  return stressScore.round().clamp(0, 100);
}
```

### 4.6. Kaloriya Hisoblash
```dart
// health_algorithm_service.dart:530
double _calculateCaloriesPerSecond(int hr) {
  // Keytel et al. formula
  double calories;
  if (_userProfile.gender == Gender.male) {
    calories = (-55.0969 + 0.6309 * hr + 0.1988 * weight + 0.2017 * age) / 4.184;
  } else {
    calories = (-20.4022 + 0.4472 * hr - 0.1263 * weight + 0.074 * age) / 4.184;
  }
  return (calories / 60); // cal/min → cal/sec
}
```

**Kaloriya Formula:**
- **Erkaklar**: `(-55.0969 + 0.6309×HR + 0.1988×Weight + 0.2017×Age) / 4.184`
- **Ayollar**: `(-20.4022 + 0.4472×HR - 0.1263×Weight + 0.074×Age) / 4.184`

---

## 🔄 5. Data Flow (Ma'lumotlar Oqimi)

### 5.1. Real-time Data Flow
```
Qurilma (BLE) 
  ↓
BLE Service (ble_health_service.dart)
  ├─ Heart Rate → _parseHeartRateData()
  ├─ SpO2 → _parseSpO2Data()
  ├─ Temperature → _parseTemperatureData()
  └─ Steps → _parseHuaweiData()
  ↓
Stream Controllers
  ├─ _heartRateController
  ├─ _spo2Controller
  └─ _temperatureController
  ↓
HealthDataProvider (health_data_provider.dart)
  ├─ Stream listeners
  ├─ _updateCalculations()
  └─ notifyListeners()
  ↓
UI (Screens)
  ├─ HomeScreen
  ├─ RecoveryDetailScreen
  ├─ StrainDetailScreen
  └─ SleepDetailScreen
```

### 5.2. Algorithm Service Integration
```
BLE Service (raw data)
  ↓
HealthAlgorithmService
  ├─ calculateRecoveryScore()
  ├─ calculateStrainScore()
  ├─ analyzeSleep()
  ├─ calculateStressLevel()
  └─ calculateDailyCalories()
  ↓
HealthDataProvider
  ├─ _recoveryScore
  ├─ _strainScore
  ├─ _sleepScore
  └─ _currentStress
  ↓
UI Updates
```

---

## 📋 6. Qaysi Ma'lumotlar Qaysi Metrikaga Ta'sir Qiladi

### 6.1. Recovery Score
**Ma'lumotlar:**
- ✅ HRV (R-R intervals) - **35%**
- ✅ Resting HR - **25%**
- ✅ Sleep Score - **25%**
- ✅ Previous Day Strain - **15%**

**Qayerdan keladi:**
- HRV: Heart Rate Service → R-R intervals → `calculateHRV()`
- Resting HR: Heart Rate readings → eng past HR (tun vaqtida)
- Sleep Score: Sleep analysis → `analyzeSleep()`
- Strain: Strain Score → `calculateStrainScore()`

### 6.2. Strain Score
**Ma'lumotlar:**
- ✅ Heart Rate (real-time) - har bir reading uchun
- ✅ HR Zone (Rest, Warmup, FatBurn, Cardio, Peak, MaxEffort)
- ✅ Activity Duration

**Qayerdan keladi:**
- Heart Rate: Heart Rate Service → `_parseHeartRateData()`
- HR Zone: `HeartRateZone.fromBPM(hr, maxHR)`
- Strain Contribution: Zone bo'yicha (0.0 - 1.50 per reading)

### 6.3. Sleep Score
**Ma'lumotlar:**
- ✅ Heart Rate (tun vaqtida)
- ✅ HR Variability (tun vaqtida)
- ✅ Sleep Duration
- ✅ Wake Events

**Qayerdan keladi:**
- Heart Rate: Heart Rate Service → tun vaqtidagi readings
- Sleep Stages: `_detectSleepStages()` → HR patterns asosida
- Sleep Performance: `_calculateSleepPerformance()`

### 6.4. Stress Level
**Ma'lumotlar:**
- ✅ HRV (RMSSD, pNN50) - **asosiy**
- ✅ Current HR vs Resting HR
- ✅ HR Variability

**Qayerdan keladi:**
- HRV: R-R intervals → `calculateHRV()`
- Current HR: Heart Rate Service → oxirgi reading
- Resting HR: Heart Rate readings → eng past HR

### 6.5. Calories
**Ma'lumotlar:**
- ✅ Heart Rate (real-time)
- ✅ User Profile (age, weight, gender)
- ✅ Activity Duration

**Qayerdan keladi:**
- Heart Rate: Heart Rate Service → har bir reading uchun
- Formula: Keytel et al. → `_calculateCaloriesPerSecond()`
- Total: BMR + Active Calories

---

## 🔧 7. Device Capabilities

### 7.1. Qurilma Aniqlash
```dart
// device_capabilities.dart
DeviceCapabilities getProfile(String deviceName) {
  if (name.contains('huawei band 8')) {
    return DeviceCapabilities(
      hasHeartRate: true,
      hasHRV: true,
      hasSpO2: true,
      hasTemperature: true,
      hasSteps: true,
      // ...
    );
  }
}
```

### 7.2. Service Discovery
```dart
// ble_health_service.dart:287
Future<void> _discoverAndSubscribe(BluetoothDevice device) {
  List<BluetoothService> services = await device.discoverServices();
  
  for (var service in services) {
    String serviceUuid = service.uuid.toString().toLowerCase();
    
    if (serviceUuid.contains('180d')) {  // Heart Rate
      await _subscribeToHeartRate(service);
    }
    if (serviceUuid.contains('1822')) {  // SpO2
      await _subscribeToSpO2(service);
    }
    if (serviceUuid.contains('1809')) {  // Temperature
      await _subscribeToTemperature(service);
    }
  }
}
```

---

## 📊 8. Real-time Updates

### 8.1. Stream Listeners
```dart
// health_data_provider.dart:176
_subscriptions.add(_bleService.heartRateStream.listen((reading) {
  _currentHR = reading.bpm;
  _hrHistory.add(reading);
  _updateCalculations();  // Recovery, Strain, Stress yangilanadi
  notifyListeners();       // UI yangilanadi
}));
```

### 8.2. Periodic Calculations
```dart
// health_data_provider.dart:166
_metricsTimer = Timer.periodic(const Duration(minutes: 5), (timer) {
  _syncMetricsToBackend();  // Backend'ga yuborish
});
```

---

## 🎯 9. Xulosa

### Ma'lumotlar Oqimi:
1. **BLE Service** → Raw binary data o'qiladi
2. **Parse Functions** → Binary → Structured data (HR, SpO2, Temp, Steps)
3. **Algorithm Service** → Structured data → Metrikalar (Recovery, Strain, Sleep, Stress)
4. **HealthDataProvider** → State management, UI updates
5. **UI Screens** → Real-time ko'rsatish

### Asosiy Metrikalar:
- **Recovery**: HRV (35%) + RestingHR (25%) + Sleep (25%) + Strain (15%)
- **Strain**: HR Zone bo'yicha cumulative strain (0.0 - 21.0)
- **Sleep**: HR patterns asosida stages (Awake, Light, Deep, REM)
- **Stress**: HRV + Current HR vs Resting HR
- **Calories**: HR-based formula (Keytel et al.)

### Real-time Updates:
- Har bir HR reading → Strain yangilanadi
- HRV hisoblash → Recovery yangilanadi
- Sleep detection → Sleep Score yangilanadi
- Stress calculation → Stress Level yangilanadi

