def storySelection(category):
    if category=="news":
        stories={}
        featureStory = storyInfo("Magnitude 6.3 Earthquake Strikes Mediterranean")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Record Powerball Jackpot"),storyInfo("Replacing UK's Trident Missile System"),storyInfo("Migrant Numbers")]
    elif category=="passion":
        stories={}
        featureStory = storyInfo("You Call That a Number?")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Astronomical Numbers"),storyInfo("Infinite Jest")]
    elif category=="education":
        stories={}
        featureStory = storyInfo("Numb about Numbers?")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("It's All Gone Non-Linear"), storyInfo("Why the Giant Spiders are Doomed"),storyInfo("The Power of a Thousand")]
    elif category=="landmark":
        stories={}
        featureStory = storyInfo("Stand on Zanzibar")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Doubling Up"),storyInfo("Plus or Minus")]
    else:
        stories={}
        featureStory = storyInfo("Wow")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Other Story"),storyInfo("More Stuffs")]
    return stories


def storyInfo(storyName):
    if storyName == "Magnitude 6.3 Earthquake Strikes Mediterranean":
        sourceLink = "http://news.sky.com/story/1628939/strong-earthquake-strikes-mediterranean"
        synopsis = "On Jan 25th 2016, between Spain and Morocco, there was a magnitude 6.3 earthquake. Is that a big earthquake? (A: Property damage but no deaths) Earthquakes are measured on a log scale which makes magnitudes hard to understand. Read on ..."
        image =""
    elif storyName == "Record Powerball Jackpot":
        sourceLink = "https://en.wikipedia.org/wiki/Lottery_jackpot_records"
        synopsis = "On Jan 13th, the US Powerball jackpot was a record £1.5864bn. BUT because there were 3 winning tickets, this has not created the world's largest ticket win. That still sits at $370.9m, a record set in May 2013."
        image =""
    elif storyName == "You Call That a Number?":
        sourceLink = "https://en.wikipedia.org/wiki/Number"
        synopsis = "self."
        image =""
    elif storyName == "It's All Gone Non-Linear":
        sourceLink = "https://en.wikipedia.org/wiki/Number"
        synopsis = "By and large we are adapted to a world of small differences and steady growth. We are comfortable with difference being a matter of subtraction. But when we stumble over exponential change, differences won't do. Things have gone Non-Linear."
        image =""
    elif storyName == "Numb about Numbers?":
        sourceLink="http://www.andrewcaelliott.com/explorations/2016/1/13/is-that-a-big-number"
        synopsis = "In 1982 Douglas Hofstadter wrote about Number Numbness. We're still befuddled in the face of millions and billions, let alone trillions or even bigger numbers. That's the reason for www.IsThatABigNumber.com."        
        image = "" 
    elif storyName == "Stand on Zanzibar":
        sourceLink="https://en.wikipedia.org/wiki/Stand_on_Zanzibar"
        synopsis = "Stand on Zanzibar is a 1968 science fiction novel by John Brunner. It takes its name from the author's projection that by 2010, if all the world's population stood shoulder to shoulder, the island of Zanzibar could accommodate them."        
        image = "" 
    else:
        sourceLink="https://www.google.com"
        synopsis = "Lorem ipsum dolor sit amet, mea et quaeque saperet, ex cum solet evertitur constituto. Nobis intellegat disputationi te duo, diam ludus nonumes mea ea. Te cum commodo appetere, ea melius dolorum sea, erat elitr corrumpit mei et. Dicunt scripta petentium eu usu."        
        image = "" 
    return {"title":storyName, "synopsis":synopsis,"links":[sourceLink]}       