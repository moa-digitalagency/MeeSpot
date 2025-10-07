#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

def check_room_access(room, user):
    """Check if a user meets room access criteria"""
    if room.access_gender and user.gender != room.access_gender:
        return False
    if room.access_orientation and user.sexual_orientation != room.access_orientation:
        return False
    
    user_age = user.calculate_age() if user.birthdate else user.age
    if room.access_age_min and user_age and user_age < room.access_age_min:
        return False
    if room.access_age_max and user_age and user_age > room.access_age_max:
        return False
    
    if room.access_meeting_type and user.meeting_type != room.access_meeting_type:
        return False
    if room.access_religion and user.religion != room.access_religion:
        return False
    if room.access_lgbtq_friendly and user.lgbtq_friendly != room.access_lgbtq_friendly:
        return False
    return True
