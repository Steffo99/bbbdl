Usage
=====

Once installed, bbbdl can be run from the command line.

bbbdl has multiple operating modes; to view them all, run:

.. code-block:: console

   $ bbbdl --help

Download mode
-------------

Download mode is used to download and render a single meeting.

This will download and render the meeting at ``MEETING_URL`` and save it as ``OUTPUT_FILE_NAME.mp4``.

.. code-block:: console

   $ bbbdl download -i MEETING_URL -o OUTPUT_FILE_NAME.mp4

You can specify a different extension as output file, and ffmpeg will render the video using that codec.

Additional options can be specified; to view the complete list, run:

.. code-block:: console

   $ bbbdl download --help

Sync mode
---------

Sync mode is used to batch download all available meetings from a list file, skipping files that were already downloaded
so to not download and render them twice.

All options can be viewed with:

.. code-block:: console

   $ bbbdl sync --help

List file
~~~~~~~~~

The list file is a JSON file, containing a single object with filenames as keys and meeting urls as values:

.. code-block:: json

   {
       "example-1.mp4": "https://example.org/playback/presentation/2.0/playback.html?meetingId=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa-1111111111111",
       "example-2.mkv": "https://example.org/playback/presentation/2.0/playback.html?meetingId=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb-2222222222222"
   }

It can be on the local machine, or available through HTTPS.

Syncing from a local list file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the JSON file is saved on your computer as `FILENAME.json`, you can sync the contents of the list file with the
current folder by running:

.. code-block:: console

   $ bbbdl sync -f FILENAME.json


Syncing from a remote list file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To sync using a JSON file provided through HTTPS, run:

.. code-block:: console

   $ bbbdl sync -r https://example.org/my-remote-list.json
