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

#### Summary
The following is a distribution of game win percentages across all odds differences where the lower payout won.
what is the odds differece?
it is the differnce in payout between the two opposite game
outcomes (ie. H and V) consider the example below:
```
 H+   H    T    V    V+
2.1  1.6  5.0  1.3  1.8  (odds difference = 0.3)
```
<iframe width="900" height="800" frameborder="0" scrolling="no" src="//plot.ly/~nikperi/10.embed"></iframe>
