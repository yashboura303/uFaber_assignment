from datetime import timedelta, datetime


class Track():
    """
    A class to manage task trakcing.

    """
    id = 0

    def __init__(self):
        """
        Attributes:

            id: to maintain the number of tracks
            talks: stores the talks which are completed
            talk_list: stores the input tasks with their respective time

        """
        Track.id += 1
        self.talks = {}
        self.talk_list = self.extract_input_from_file()

    def extract_input_from_file(self):
        """
        This function reads the lines from the text input file and stores all tasks in 
        dictionary with their respective time. (negative indexing raises error, so it means it's lightning)
        """
        talks = {}
        lines = []
        try:
            lines = [line.strip() for line in open('input.txt')]
        except FileNotFoundError as e:
            print('File Not Found', e)
        for line in lines:
            title, minutes = line.rsplit(maxsplit=1)
            try:
                minutes = int(minutes[:-3])
            except ValueError:
                minutes = 5
            talks[line] = minutes
        return talks

    def get_talks(self, start_talk, end_talk):
        """
        Only if the task time is less than the end time then it is added to the 'task' and consequently that task is remvoed from 'talk_list'

        Parameters:
            start_talk (int): Starting hour
            end_talk (int): Ending hour
        Returns:
            talks (dic): Dictionary of talks and their respective time
        """
        start = timedelta(hours=start_talk)
        for talk, minutes in list(self.talk_list.items()):
            prev = start + timedelta(minutes=int(minutes))
            if prev <= timedelta(hours=end_talk):
                self.talks[(datetime.min + start).strftime('%I:%M %p')] = talk
                self.talk_list.popitem()
                start += timedelta(minutes=int(minutes))
        return self.talks

    def time_after_start(self, hours):
        """
        Returns lunch time or networking event time in the required format.

        Parameters:
            hours (int): hour to be formatted
        Returns:
            Time in required format
        """
        return (datetime.min + timedelta(hours=hours)).strftime('%I:%M %p')

    def show_output(self):
        """
        This function calls prepare_output and time_after_start functions until all the tasks are read
        """
        while len(self.talk_list) != 0:
            print(f'Track {Track.id}')
            self.prepare_output(9, 12)
            print(f'{self.time_after_start(12)} - Lunch')
            self.prepare_output(13, 17)
            print(f'{self.time_after_start(17)} - Networking Event')
            Track.id += 1

    def prepare_output(self, start, end):
        """
        This function requires start and end time hour to print the tasks in sorted manner by calling get_talks function. Also it clears previous entries

        Parameters:
            start_talk (int): Starting hour
            end_talk (int): Ending hour
        """
        for time, title in sorted(self.get_talks(start, end).items()):
            print(time, '-', title)
        self.talks.clear()


if __name__ == '__main__':
    a = Track()
    a.show_output()
