import asyncio

from nltk import text
from utils import get_chars, get_places, get_summary

text = """
Mr. and Mrs. Dursley, of number four, Privet Drive, were proud to say
that they were perfectly normal, thank you very much. They were the last
people you'd expect to be involved in anything strange or mysterious,
because they just didn't hold with such nonsense.
Mr. Dursley was the director of a firm called Grunnings, which made
drills. He was a big, beefy man with hardly any neck, although he did
have a very large mustache. Mrs. Dursley was thin and blonde and had
nearly twice the usual amount of neck, which came in very useful as she
spent so much of her time craning over garden fences, spying on the
neighbors. The Dursleys had a small son called Dudley and in their
opinion there was no finer boy anywhere.
The Dursleys had everything they wanted, but they also had a secret, and
their greatest fear was that somebody would discover it. They didn't
think they could bear it if anyone found out about the Potters. Mrs.
Potter was Mrs. Dursley's sister, but they hadn't met for several years;
in fact, Mrs. Dursley pretended she didn't have a sister, because her
sister and her good-for-nothing husband were as unDursleyish as it was
possible to be. The Dursleys shuddered to think what the neighbors would
say if the Potters arrived in the street. The Dursleys knew that the
Potters had a small son, too, but they had never even seen him. This boy
was another good reason for keeping the Potters away; they didn't want
Dudley mixing with a child like that.
When Mr. and Mrs. Dursley woke up on the dull, gray Tuesday our story
starts, there was nothing about the cloudy sky outside to suggest that
strange and mysterious things would soon be happening all over the
country. Mr. Dursley hummed as he picked out his most boring tie for
work, and Mrs. Dursley gossiped away happily as she wrestled a screaming
Dudley into his high chair.
None of them noticed a large, tawny owl flutter past the window.
At half past eight, Mr. Dursley picked up his briefcase, pecked Mrs.
Dursley on the cheek, and tried to kiss Dudley good-bye but missed,
2
because Dudley was now having a tantrum and throwing his cereal at the
walls. "Little tyke," chortled Mr. Dursley as he left the house. He got
into his car and backed out of number four's drive.
It was on the corner of the street that he noticed the first sign of
something peculiar -- a cat reading a map. For a second, Mr. Dursley
didn't realize what he had seen -- then he jerked his head around to
look again. There was a tabby cat standing on the corner of Privet
Drive, but there wasn't a map in sight. What could he have been thinking
of? It must have been a trick of the light. Mr. Dursley blinked and
stared at the cat. It stared back. As Mr. Dursley drove around the
corner and up the road, he watched the cat in his mirror. It was now
reading the sign that said Privet Drive -- no, looking at the sign; cats
couldn't read maps or signs. Mr. Dursley gave himself a little shake and
put the cat out of his mind. As he drove toward town he thought of
nothing except a large order of drills he was hoping to get that day.
But on the edge of town, drills were driven out of his mind by something
else. As he sat in the usual morning traffic jam, he couldn't help
noticing that there seemed to be a lot of strangely dressed people
about. People in cloaks. Mr. Dursley couldn't bear people who dressed in
funny clothes -- the getups you saw on young people! He supposed this
was some stupid new fashion. He drummed his fingers on the steering
wheel and his eyes fell on a huddle of these weirdos standing quite
close by. They were whispering excitedly together. Mr. Dursley was
enraged to see that a couple of them weren't young at all; why, that man
had to be older than he was, and wearing an emerald-green cloak! The
nerve of him! But then it struck Mr. Dursley that this was probably some
silly stunt -- these people were obviously collecting for something...
yes, that would be it. The traffic moved on and a few minutes later, Mr.
Dursley arrived in the Grunnings parking lot, his mind back on drills.
Mr. Dursley always sat with his back to the window in his office on the
ninth floor. If he hadn't, he might have found it harder to concentrate
on drills that morning. He didn't see the owls swoop ing past in broad
daylight, though people down in the street did; they pointed and gazed
open- mouthed as owl after owl sped overhead. Most of them had never
seen an owl even at nighttime. Mr. Dursley, however, had a perfectly
normal, owl-free morning. He yelled at five different people. He made
several important telephone calls and shouted a bit more. He was in a
very good mood until lunchtime, when he thought he'd stretch his legs
and walk across the road to buy himself a bun from the bakery.
"""

import requests
import json


def send_request(text):
    url = "http://127.0.0.1:8000/completions/"
    headers = {"Content-Type": "application/json", "Authorization": "FAKETOKEN"}

    payload = {
        "model": "string",
        "messages": [{"role": "User", "content": text}],
        "max_tokens": 1000,
        "stream": False,
        "temperature": 0,
        "top_p": 0,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    send_request(text)
