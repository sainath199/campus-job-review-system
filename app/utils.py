from app import db
from app.models import Reviews, Notification, User
from sqlalchemy.sql import func
from datetime import datetime

def notify_users_about_new_job(job_title):
    """
    Create notifications for all users about a newly posted job.
    """
    users = User.query.all()  # Fetch all users
    message = f"A new job titled '{job_title}' has been posted. Check it out!"

    for user in users:
        notification = Notification(user_id=user.id, message=message, timestamp=datetime.utcnow())
        db.session.add(notification)

    db.session.commit()
    print(f"Notifications created for {len(users)} users.")

def get_all_jobs_statistics():
    """
    Calculate review statistics for all jobs based on the Reviews table.
    """
    job_stats = []
    # Fetch unique job titles from the Reviews table
    job_titles = db.session.query(Reviews.job_title).distinct()

    for job_title in job_titles:
        # Fetch statistics for each job title
        stats = get_review_statistics(job_title[0])  # job_title[0] to extract the string
        stats["job_title"] = job_title[0]
        job_stats.append(stats)

    return job_stats

def get_review_statistics(job_title):
    """
    Calculate review statistics for a given job title from the Reviews table.
    """
    # Total reviews for the job title
    total_reviews = db.session.query(func.count(Reviews.id)).filter(Reviews.job_title == job_title).scalar()

    # Positive reviews (recommendation >= 6)
    positive_reviews = db.session.query(func.count(Reviews.id)).filter(
        Reviews.job_title == job_title, Reviews.recommendation >= 6
    ).scalar()

    # Negative reviews (recommendation <= 5)
    negative_reviews = total_reviews - positive_reviews

    # Average rating
    average_rating = db.session.query(func.avg(Reviews.rating)).filter(
        Reviews.job_title == job_title
    ).scalar() or 0

    # Job score out of 5 (round the average rating)
    job_score = round(average_rating)

    return {
        "total_reviews": total_reviews,
        "positive_reviews": positive_reviews,
        "negative_reviews": negative_reviews,
        "average_rating": average_rating,
        "job_score": job_score,
    }

