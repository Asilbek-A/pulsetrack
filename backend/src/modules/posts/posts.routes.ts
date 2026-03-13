import { Router, Request, Response } from 'express';
import { AppDataSource } from '../../infra/data-source';
import { Post, PostPrivacy, PostType, PostLike, PostComment } from './post.entity';
import { authMiddleware } from '../auth/authMiddleware';

const router = Router();

// Create post
router.post('/', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const {
      type,
      privacy,
      content,
      workoutType,
      distance,
      durationSeconds,
      avgHeartRate,
      maxHeartRate,
      calories,
      strain,
      avgSpeed,
      elevationGain,
      route,
      mapImageUrl,
    } = req.body;

    const postRepo = AppDataSource.getRepository(Post);
    const post = postRepo.create({
      userId,
      type: type || PostType.WORKOUT,
      privacy: privacy || PostPrivacy.PRIVATE,
      content,
      workoutType,
      distance,
      durationSeconds,
      avgHeartRate,
      maxHeartRate,
      calories,
      strain,
      avgSpeed,
      elevationGain,
      route,
      mapImageUrl,
    });

    await postRepo.save(post);
    
    res.status(201).json(post);
  } catch (error) {
    console.error('Create post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get posts (with filtering)
router.get('/', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { privacy, limit = '20', offset = '0' } = req.query;

    const postRepo = AppDataSource.getRepository(Post);
    const queryBuilder = postRepo.createQueryBuilder('post')
      .leftJoinAndSelect('post.user', 'user')
      .orderBy('post.createdAt', 'DESC')
      .skip(Number(offset))
      .take(Number(limit));

    // Filter by privacy
    if (privacy === 'public') {
      queryBuilder.where('post.privacy = :privacy', { privacy: PostPrivacy.PUBLIC_ALL });
    } else if (privacy === 'community') {
      // TODO: Add friends/community logic
      queryBuilder.where('post.privacy IN (:...privacies)', {
        privacies: [PostPrivacy.PUBLIC_ALL, PostPrivacy.COMMUNITY],
      });
    } else if (privacy === 'mine') {
      queryBuilder.where('post.userId = :userId', { userId });
    } else {
      // Default: public + community
      queryBuilder.where('post.privacy IN (:...privacies)', {
        privacies: [PostPrivacy.PUBLIC_ALL, PostPrivacy.COMMUNITY],
      });
    }

    const posts = await queryBuilder.getMany();
    
    res.json(posts);
  } catch (error) {
    console.error('Get posts error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get single post
router.get('/:id', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const postRepo = AppDataSource.getRepository(Post);
    
    const post = await postRepo.findOne({
      where: { id },
      relations: ['user', 'likes', 'comments'],
    });

    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    res.json(post);
  } catch (error) {
    console.error('Get post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Update post
router.put('/:id', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { id } = req.params;
    const { content, privacy } = req.body;

    const postRepo = AppDataSource.getRepository(Post);
    const post = await postRepo.findOne({ where: { id } });

    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    if (post.userId !== userId) {
      return res.status(403).json({ message: 'Not authorized' });
    }

    if (content !== undefined) post.content = content;
    if (privacy !== undefined) post.privacy = privacy;

    await postRepo.save(post);
    
    res.json(post);
  } catch (error) {
    console.error('Update post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Delete post
router.delete('/:id', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { id } = req.params;

    const postRepo = AppDataSource.getRepository(Post);
    const post = await postRepo.findOne({ where: { id } });

    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    if (post.userId !== userId) {
      return res.status(403).json({ message: 'Not authorized' });
    }

    await postRepo.remove(post);
    
    res.json({ message: 'Post deleted' });
  } catch (error) {
    console.error('Delete post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Like post
router.post('/:id/like', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { id } = req.params;

    const postRepo = AppDataSource.getRepository(Post);
    const likeRepo = AppDataSource.getRepository(PostLike);

    const post = await postRepo.findOne({ where: { id } });
    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    // Check if already liked
    const existing = await likeRepo.findOne({
      where: { postId: id, userId },
    });

    if (existing) {
      return res.status(400).json({ message: 'Already liked' });
    }

    const like = likeRepo.create({ postId: id, userId });
    await likeRepo.save(like);

    // Update post likes count
    post.likesCount += 1;
    await postRepo.save(post);

    res.status(201).json({ message: 'Post liked' });
  } catch (error) {
    console.error('Like post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Unlike post
router.delete('/:id/like', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { id } = req.params;

    const postRepo = AppDataSource.getRepository(Post);
    const likeRepo = AppDataSource.getRepository(PostLike);

    const like = await likeRepo.findOne({
      where: { postId: id, userId },
    });

    if (!like) {
      return res.status(404).json({ message: 'Like not found' });
    }

    await likeRepo.remove(like);

    // Update post likes count
    const post = await postRepo.findOne({ where: { id } });
    if (post) {
      post.likesCount = Math.max(0, post.likesCount - 1);
      await postRepo.save(post);
    }

    res.json({ message: 'Post unliked' });
  } catch (error) {
    console.error('Unlike post error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Add comment
router.post('/:id/comments', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { id } = req.params;
    const { content } = req.body;

    if (!content || content.trim().length === 0) {
      return res.status(400).json({ message: 'Comment content required' });
    }

    const postRepo = AppDataSource.getRepository(Post);
    const commentRepo = AppDataSource.getRepository(PostComment);

    const post = await postRepo.findOne({ where: { id } });
    if (!post) {
      return res.status(404).json({ message: 'Post not found' });
    }

    const comment = commentRepo.create({
      postId: id,
      userId,
      content: content.trim(),
    });

    await commentRepo.save(comment);

    // Update post comments count
    post.commentsCount += 1;
    await postRepo.save(post);

    // Load user info for response
    const savedComment = await commentRepo.findOne({
      where: { id: comment.id },
      relations: ['user'],
    });

    res.status(201).json(savedComment);
  } catch (error) {
    console.error('Add comment error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Get comments
router.get('/:id/comments', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const commentRepo = AppDataSource.getRepository(PostComment);

    const comments = await commentRepo.find({
      where: { postId: id },
      relations: ['user'],
      order: { createdAt: 'ASC' },
    });

    res.json(comments);
  } catch (error) {
    console.error('Get comments error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

// Delete comment
router.delete('/:postId/comments/:commentId', authMiddleware, async (req: Request, res: Response) => {
  try {
    const userId = (req as any).userId;
    const { postId, commentId } = req.params;

    const postRepo = AppDataSource.getRepository(Post);
    const commentRepo = AppDataSource.getRepository(PostComment);

    const comment = await commentRepo.findOne({
      where: { id: commentId, postId },
    });

    if (!comment) {
      return res.status(404).json({ message: 'Comment not found' });
    }

    if (comment.userId !== userId) {
      return res.status(403).json({ message: 'Not authorized' });
    }

    await commentRepo.remove(comment);

    // Update post comments count
    const post = await postRepo.findOne({ where: { id: postId } });
    if (post) {
      post.commentsCount = Math.max(0, post.commentsCount - 1);
      await postRepo.save(post);
    }

    res.json({ message: 'Comment deleted' });
  } catch (error) {
    console.error('Delete comment error:', error);
    res.status(500).json({ message: 'Server error' });
  }
});

export default router;

