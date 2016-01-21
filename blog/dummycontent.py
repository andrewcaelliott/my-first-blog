def storySelection(category):
    if category=="news":
        stories={}
        featureStory = storyInfo("Record Powerball Jackpot")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("News Story"),storyInfo("More News")]
    elif category=="passion":
        stories={}
        featureStory = storyInfo("You Call That a Number?")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Fun Story"),storyInfo("More Fun")]
    elif category=="education":
        stories={}
        featureStory = storyInfo("It's Gone Non-Linear")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Education Story"),storyInfo("More Education")]
    elif category=="landmark":
        stories={}
        featureStory = storyInfo("Stand on Zanzibar")
        stories["featured"]=featureStory
        stories["other"]=[storyInfo("Landmark Story"),storyInfo("More Landmark")]
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
    else:
        sourceLink="http://www.google.com"
        synopsis = "Lorem ipsum dolor sit amet, vim et equidem officiis, vis verear splendide disputando no. Usu at sanctus phaedrum periculis, eu nec tale reprimique. "        
        image = "" 
    return {"title":storyName, "synopsis":synopsis,"link":sourceLink}       