def storySelection(category):
    if category=="news":
        stories={}
        featureStory = storyInfo("Record Powerball Jackpot")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Replacing UK's Trident Missile System"),storyInfo("Migrant Numbers")]
    elif category=="passion":
        stories={}
        featureStory = storyInfo("You Call That a Number?")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Really, Really Big Numbers"),storyInfo("Infinite Jest")]
    elif category=="education":
        stories={}
        featureStory = storyInfo("It's All Gone Non-Linear")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Why the Giant Spiders are Doomed"),storyInfo("The Joy of Logs")]
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
    if storyName == "Record Powerball Jackpot":
        sourceLink = "https://en.wikipedia.org/wiki/Lottery_jackpot_records"
        synopsis = "On Jan 13th, the US Powerball jackpot was a record £1.5864bn. BUT because there were 3 winning tickets, this has not created the world's largest ticket win. That still sits at $370.9m, a record set in May 2013."
        image =""
    elif storyName == "You Call That a Number?":
        sourceLink = "https://en.wikipedia.org/wiki/Number"
        synopsis = "It starts with counting: 1, 2, 3 are what the maths guys call the Natural Numbers. From there it gets more and more UN-natural, all the way to imaginary and beyond, to some very weird structures that still get called 'numbers'."
        image =""
    elif storyName == "It's All Gone Non-Linear":
        sourceLink = "https://en.wikipedia.org/wiki/Number"
        synopsis = "By and large we are adapted to a world of small differences and steady growth. We are comfortable with difference being a matter of subtraction. But when we stumble over exponential change, differences won't do. Things have gone Non-Linear."
        image =""
    elif storyName == "Stand on Zanzibar":
        sourceLink="https://en.wikipedia.org/wiki/Stand_on_Zanzibar"
        synopsis = "Stand on Zanzibar is a 1968 science fiction novel by John Brunner. It takes its name from the author's projection that by 2010, if all the world's population stood shoulder to shoulder, the island of Zanzibar could accommodate them."        
        image = "" 
    else:
        sourceLink="https://www.google.com"
        synopsis = "Lorem ipsum dolor sit amet, mea et quaeque saperet, ex cum solet evertitur constituto. Nobis intellegat disputationi te duo, diam ludus nonumes mea ea. Te cum commodo appetere, ea melius dolorum sea, erat elitr corrumpit mei et. Dicunt scripta petentium eu usu."        
        image = "" 
    return {"title":storyName, "synopsis":synopsis,"link":sourceLink}       