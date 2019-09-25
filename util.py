from random import randrange

users = [
  'Ashley',
  'Bill',
  'Chris',
  'Dominic',
  'Emma',
  'Faizan',
  'Gimmy',
  'Harry',
  'Ian',
  'John',
  'King',
  'Lisa',
  'Mona',
  'Nina',
  'Olivia',
  'Pete',
  'Queen',
  'Robert',
  'Sarah',
  'Tierra',
  'Una',
  'Varun',
  'Will',
  'Xin',
  'You',
  'Zeba'
]

def get_user():
  return users

def get_random_number():
  return randrange(len(users) - 1)

def get_random_user():
  return users[get_random_number()]
