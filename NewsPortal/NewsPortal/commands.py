from django.contrib.auth.models import User
user1 = User.objects.create_user('username1')
user2 = User.objects.create_user('username2')

author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

category1 = Category.objects.create(name='Category 1')
category2 = Category.objects.create(name='Category 2')
category3 = Category.objects.create(name='Category 3')
category4 = Category.objects.create(name='Category 4')

post1 = Post.objects.create(author=author1, title='Post 1', content='This is post 1 content')
post2 = Post.objects.create(author=author2, title='Post 2', content='This is post 2 content')
news1 = News.objects.create(author=author1, title='News 1', content='This is news 1 content')

post1.categories.add(category1, category2)
news1.categories.add(category3, category4)

comment1 = Comment.objects.create(post=post1, user=user1, content='This is comment 1')
comment2 = Comment.objects.create(post=post1, user=user2, content='This is comment 2')
comment3 = Comment.objects.create(post=post2, user=user1, content='This is comment 3')
comment4 = Comment.objects.create(post=post2, user=user2, content='This is comment 4')

post1.like()
post2.dislike()
comment1.like()
comment3.dislike()

author1.update_rating()
author2.update_rating()

best_author = Author.objects.order_by('-rating').first()
print(f'Best user: {best_author.user.username}, Rating: {best_author.rating}')

best_post = Post.objects.filter(news=False).order_by('-rating').first()
print(f'Date: {best_post.created_at}')
print(f'Author: {best_post.author.user.username}')
print(f'Rating: {best_post.rating}')
print(f'Title: {best_post.title}')
print(f'Preview: {best_post.preview()}')

comments = Comment.objects.filter(post=best_post)
for comment in comments:
    print(f'Date: {comment.created_at}')
    print(f'User: {comment.user.username}')
    print(f'Rating: {comment.rating}')
    print(f'Content: {comment.content}')