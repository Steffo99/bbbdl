import requests
import ffmpeg
import click
import json
import os
from .resources import Meeting
from .composer import compose_lesson


@click.group()
def main():
    pass


@main.command()
@click.option("-i", "--input-url", type=str, prompt=True,
              help="The URL of the meeting to download.")
@click.option("-o", "--output-file", type=str, prompt=True,
              help="The file the video should be written to.")
@click.option("-O", "--overwrite", is_flag=True,
              help="Overwrite existing files instead of skipping them.")
@click.option("-v", "--verbose-ffmpeg", is_flag=True,
              help="Print ffmpeg info to stderr.")
@click.option("-D", "--debug", is_flag=True,
              help="Print the compiled ffmpeg command to stdout instead of running it.")
def download(input_url, output_file, overwrite=False, verbose_ffmpeg=False, debug=False):
    if not overwrite and os.path.exists(output_file):
        raise click.ClickException(f"Output file already exists: {output_file}")

    meeting = Meeting.from_url(input_url)

    click.secho(f"Downloading: {input_url} -> {output_file}", err=True, fg="green")
    tracks = compose_lesson(meeting, 1280, 720)

    output = ffmpeg.output(tracks.video, tracks.audio, output_file)

    if debug:
        click.echo(" ".join(output.compile()))

    try:
        output.run(quiet=not verbose_ffmpeg, overwrite_output=True)
    except FileNotFoundError:
        raise click.ClickException("ffmpeg is not installed!\nPlease download it at https://ffmpeg.org/download.")


@main.command()
@click.option("-f", "--file", type=click.File(),
              help="The JSON file containing the files to download.")
@click.option("-r", "--remote-file", type=str,
              help="The URL where the JSON file containing the files to download can be fetched.")
@click.option("-O", "--overwrite", is_flag=True,
              help="Overwrite existing files instead of skipping them.")
@click.option("-v", "--verbose-ffmpeg", is_flag=True,
              help="Print ffmpeg info to stderr.")
@click.pass_context
def sync(ctx: click.Context, file=None, remote_file=None, overwrite=False, verbose_ffmpeg=False):
    if file:
        click.secho(f"Syncing from local file: {file.name}", err=True, bold=True, bg="white", fg="black")
        j = json.load(file)
    elif remote_file:
        click.secho(f"Syncing from remote file: {remote_file}", err=True, bold=True)
        j = requests.get(remote_file).json()
    else:
        raise click.ClickException("No JSON file was specified.")

    for output_file, input_url in j.items():
        try:
            ctx.invoke(download, input_url=input_url, output_file=output_file, overwrite=overwrite, verbose_ffmpeg=verbose_ffmpeg)
        except click.ClickException:
            click.secho(f"Skipped: {input_url} -> {output_file}", err=True, fg="cyan")
        except requests.HTTPError as e:
            click.secho(f"Not available: {input_url} -> HTTP {e.response.status_code}", err=True, fg="yellow")


if __name__ == "__main__":
    main()
