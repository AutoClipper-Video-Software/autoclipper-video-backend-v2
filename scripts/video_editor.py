import moviepy.editor as mpy
from moviepy.editor import VideoFileClip, CompositeVideoClip
from subtitles_parser import parse_subtitles


def create_clip_from_video(
    clip_start: float, clip_end: float, video_file_path: str
) -> VideoFileClip:
    """Simply generates a clip of a section of a given video using MoviePy.
    \n
    Returns the generated clip as a `VideoFileClip`."""

    clip: mpy.VideoFileClip = mpy.VideoFileClip(video_file_path).subclip(
        clip_start, clip_end
    )

    return clip


def fits_frame(line_count, font, font_size, stroke_width, frame_width):
    def fit_function(text):
        lines = calculate_lines(text, font, font_size, stroke_width, frame_width)
        return len(lines["lines"]) <= line_count

    return fit_function


def add_captions_to_video(
    video_file: str,
    subtitles,
    highlight_current_word: bool,
    word_highlight_color: str,
    font: str,
    font_size: int,
    font_color: str,
    stroke_width: int,
    line_count: int,
    padding: int,
):
    # Code based on https://github.com/unconv/captacity/blob/master/captacity/__init__.py

    font_path = f"fonts/{font}"

    video = VideoFileClip(video_file)
    text_bbox_width = video.w - padding * 2
    clips = [video]

    captions = parse_subtitles(
        segments=subtitles,
        fit_function=fits_frame(
            line_count, font, font_size, stroke_width, text_bbox_width
        ),
    )

    for caption in captions:
        captions_to_draw = []

        if highlight_current_word:
            for i, word in enumerate(caption["words"]):
                if i + 1 < len(caption["words"]):
                    end = caption["words"][i + 1]["start"]
                else:
                    end = word["end"]

                captions_to_draw.append(
                    {
                        "text": caption["text"],
                        "start": word["start"],
                        "end": end,
                    }
                )
        else:
            captions_to_draw.append(caption)

        for current_index, caption in enumerate(captions_to_draw):
            line_data = calculate_lines(
                caption["text"], font, font_size, stroke_width, text_bbox_width
            )

            text_y_offset = video.h // 2 - line_data["height"] // 2
            index = 0

            for line in line_data["lines"]:
                pos = ("center", text_y_offset)

                words = line["text"].split()
                word_list = []
                for w in words:
                    word_obj = Word(w)
                    if highlight_current_word and index == current_index:
                        word_obj.set_color(word_highlight_color)
                    index += 1
                    word_list.append(word_obj)

                text = create_text_ex(
                    word_list,
                    font_size,
                    font_color,
                    font,
                    stroke_color="black",
                    stroke_width=stroke_width,
                )
                text = text.set_start(caption["start"])
                text = text.set_duration(caption["end"] - caption["start"])
                text = text.set_position(pos)
                clips.append(text)

                text_y_offset += line["height"]

                video_with_subtitles = CompositeVideoClip(clips)

                # TODO: Write the video to a folder called "edited_clips"

                video_with_subtitles.write_videofile(
                    filename=output_file_name,
                    codec="libx264",
                    fps=video.fps,
                    logger=None,
                )
