# ReallySwellGuys-TPG2.0

This repository holds the code for the Really Swell Guys Team

# Goals / Features
1. Create a standard route sheet
2. Create a notification system w/ estimates given a route and known driver/historical data

## Coding standards
Look at Google coding standards [here](https://google.github.io/styleguide/pyguide.html)
main takeaways for basic file structure:
* Indent with 4 spaces
* No trailing whitespace
* inline comments start with '#'
* single quotes for string literals

Other important notes:
* Don't hardcode values
* Don't commit data! Don't do this on your local repo either


## To contribute do the following:
A somewhat more detailed approach to github repo management can be found [here](https://gist.github.com/Chaser324/ce0505fbed06b947d962)

### Setup
1. Fork this repo to your personal github
2. Clone your repo to your machine
3. Branch off of master
4. fetch upstream (dev or master) and checkout to your dev branch before making any changes

### When creating a feature:
1. Fetch upstream and rebase (if necessary)
2. (potentially) create a branch, this isn't strictly necessary
3. HACK
  * if you have a complex feature you may need to do several commits..
4. Clean up and squash your commits (check out the detailed approach above)
5. Push upstream
6. Pull Request to Master in GitHub
7. Merge
8. Success!
