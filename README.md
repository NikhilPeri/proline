# Proline Project
### What is the Proline Project?
[Proline](https://www.proline.ca/) is a sportsbetting game in Ontario Canada.  The Proline Project is a data study to find sucessful stratagies for the proline game.  The project is broken down into several stages:
* collect Data
* determine Sucess Probablility distribution over payouts
* determine Sucess Probability distribution over
* monitor convergence of data set
* Simulate stratagies over historical data set

#### Collect Data
The `update.py` script hits the following two OLG endpoints to fetch payouts and outcomes:

**payouts ->** proline.ca/olg-proline-services/rest/api/proline/events/all.jsonp?callback=_jqjsp&__timenow__

**outcomes ->** proline.ca/olg-proline-services/rest/api/proline/results/all.jsonp?callback=_jqjsp&__timenow__

This data is collected daily and stored in the following json format:
```
{
 <ticketID> : {
    "date": <epochDate>,
    "games": {
      <gameID>: {
        "cutoffDate", <last day to wager>,
        "sport": <sportName>,
        "visitor": <visitor team>,
        "home": <home team>,
        "h+": <home shutout payout>,
        "h": <home payout>,
        "t": <tie payout>,
        "v": <visitor payout>,
        "v+": <visitor shutout payout>,
        "outcome": [<list of payouts won>]
      },
      ...
}
```
#### The objective
The following are the rules of proline I would like to
highlight:
* proline requires you to pick three events
* the lowest possible payout for a single event being 1
* the lowest possible payout for a card being 3

If we apply [Poker Pot Odds](https://en.wikipedia.org/wiki/Pot_odds)
to these payouts and odd, we must be able to pick the outcome of a card
at least 1/3 of the time to be profitable.  Considering each game to be
an independant event we must be able to predict it with a certianty of
only 69.33% to break even in the worst case scenario.  

#### Initial Findings
The following is a distribution of game win percentages across
all odds differences where the lower payout won.
what is the odds differece?
it is the differnce in payout between the two opposite game
outcomes (ie. H and V) consider the example below:
```
 H+   H    T    V    V+
2.1  1.6  5.0  1.3  1.8  (odds difference = 0.3)
```

[[embed url=http://www.plot.ly/~nikperi/10.embed]]

It is also important to account for the number of events
observed when considering the results above. As you can see
move events of lower odd difference did occur, which is
important to consider when reading the percentages shown
above

[[embed url=http://www.plot.ly/~nikperi/14.embed]]

The permilinary findings show that events of higher
odd difference show the lower odds win more often.

NOTE:  All the findings above include all proline sports, except soccer
this is due to the rule that if a soccer game is goes into overtime it
is only payed out as a tie. While other sports payout the tie as well
as payout for the winning team


#### MLB Season
With MLB season warming up, I will be collecting short and long term
season data and ploting its relationship to proline winnings in hopes
of finding a correlation.  I want to focus more on MLB because the
seasons have more games (ie. moarrr data)

Stay tuned for more events containing the following json data
```
{
 <ticketID> : {
   ...
   "mlb_standings": {
     "home": {
       "rank": <league ranking>
       "win_percentage": <percentage of home wins>,
       "last_five_won": <number of games won in last 10>,
       "last_five_loss": <number of games lost in last 10>,
       "last_ten_won": <number of games won in last 10>,
       "last_ten_loss": <number of games lost in last 10>,
       "streak": <current consecutive wins or losses (+ve for wins -ve for losses)>
     },
     "visitor": {
       "rank": <league ranking>
       "win_percentage": <percentage of away wins>,
       "last_five_won": <number of games won in last 10>,
       "last_five_loss": <number of games lost in last 10>,
       "last_ten_won": <number of games won in last 10>,
       "last_ten_loss": <number of games lost in last 10>,
       "streak": <current consecutive wins or losses (+ve for wins -ve for losses)>
     }
   }
 }
```

#### Long term
It is still to early to apply any ML techniques to this data till
strong enough correlations are seen across a large enough dataset,
and an informed decision can
be made on the inputs.  But the long term objective is to combine
the proline odds with basic league standings from the short and
long term for a model
