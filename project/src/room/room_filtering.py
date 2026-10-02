def filter_main_rooms(
        rooms,
        min_width_threshold,
        min_height_threshold
):
    main_rooms = []
    for room in rooms:
        if (room.rect.width >= min_width_threshold and
            room.rect.height >= min_height_threshold):
            room.color = "green"
            main_rooms.append(room)
        else:
            room.color = "grey"

    return main_rooms