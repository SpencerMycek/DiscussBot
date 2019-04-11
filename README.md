# DiscussBot
A Slack application written in python that uses a bot to format discussions

## Why a DiscussBot?
This slack application was born out of the need for a way to have a clean discussion at any time. In particular, the organization I am in, Computer Science House (CSH), has a meeting every week going over news, happenings, and house based discussion. A member said at one of these meeting how unfortunate it was that we could only ever had house-wide discussions at these meetings. A standard channel on slack may eventually become cluttered or unfocused, so I took it upon myself to create an application that will remove clutter, format messages, and keep focus in the channel itself.

## What I wanted to learn
I already knew a base level of python. But I had never interacted with an API, I had never touched regex, I had barely touched JSON objects, and I wanted to get better at understanding user interaction.

### What I learned
I became more fluent with python 3.7. Which was important to me due to the ease of use of python, but I had never before attempted a complicated python project

I also learned more about APIs. I learned about restAPIs and I learned how they accept information and how Slack manages permissions with its API, which seems to be similar in other APIs I have looked at.

Regex is a terrifying beast, I have learned. But through this project I've become more skilled at reading , writing, and understanding patterns. I think in the future I will be able to more easily add regex into my projects, since it can be such an amazing help to improve workflow.

I have spent some time in prior projects worrying about how a user might interact with my application/website. However I never had to think about how a user would interact with something that in turn was interacting with them. I had to think about how people would see information and interact with it. This part I believe was one of the more fun parts of the project: Being able to work to better how my project worked as well as the general flow of using the application might occur.

## Some difficulties
The slack API has a specific way to authenticate and it has different permission for different methods and action. I had issues with auth, permissions, and how to create the right functionality in my application.
I can't say there was a major breakthrough point of getting the application to function. It was a battle all throughout working on this project.

I also had to work around issues with unicode and ascii. A mobile device, at the very least an Iphone, inserts the unicode value for apostrophes instead of an ascii value. Slack can handle this, but in my python code it wouldn't decode it correctly if any other non unicode characters were in the string. Eventually, after regex pattern and encoding/decoding methods later, I had to just remove the unicode from the string. In the future I want to revisit the issue and get it to decode the unicode properly.

## Things I want to add
In the future I want to add persistent storage and discussion archiving. As well as improve the overall look of the bot.
As I spend more time on this project I hope that CSH members will be able to use it to have discussions throughout the week instead of just a once-a-week-basis.
