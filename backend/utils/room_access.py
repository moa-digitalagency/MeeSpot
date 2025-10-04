def check_room_access(room, user):
    """Check if a user meets room access criteria"""
    if room.access_gender and user.gender != room.access_gender:
        return False
    if room.access_orientation and user.orientation != room.access_orientation:
        return False
    if room.access_age_min and user.age and user.age < room.access_age_min:
        return False
    if room.access_age_max and user.age and user.age > room.access_age_max:
        return False
    return True
