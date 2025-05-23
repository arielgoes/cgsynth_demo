import itertools

def hash_string_to_seed(s):
    hash_ = 5381
    for c in s:
        hash_ = ((hash_ << 5) + hash_) + ord(c)
    return abs(hash_) % 4294967296

def seeded_random(seed):
    state = seed
    while True:
        state = (state * 1664525 + 1013904223) % 4294967296
        yield state / 4294967296

def select_random_pairs_with_seed(pairs, count, seed):
    pairs_copy = pairs[:]
    selected = []
    rand_gen = seeded_random(seed)
    count = min(count, len(pairs_copy))
    for _ in range(count):
        idx = int(next(rand_gen) * len(pairs_copy))
        selected.append(pairs_copy.pop(idx))
    return selected

# Replace with the same list of videos used in the session (order matters!)
videos = [
    "videos/TEMP_TEST.mp4",
    "videos/interpolated_video_addWeighted.mp4",
    "videos/interpolated_video_film.mp4",
    "videos/original_video.mp4",
    "videos/original_video_1280_720.mp4",
    "videos/original_video_upsampled_from_1280_720_to_1920_1080.mp4",
    "videos/interpolated_rife_1280_720_30fps.mp4",
    "videos/video_with_degrad_mk11_1080p.mp4"
]

user_id = "5s7jpj0fUg"
user_seed = hash_string_to_seed(user_id)

# All unique unordered pairs (A != B)
all_pairs = []
for i in range(len(videos)):
    for j in range(i + 1, len(videos)):
        all_pairs.append((videos[i], videos[j]))

selected_pairs = select_random_pairs_with_seed(all_pairs, 5, user_seed)

for idx, (a, b) in enumerate(selected_pairs, 1):
    print(f"Pair {idx}: {a} vs {b}")