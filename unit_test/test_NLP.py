import unittest
from nlp import NLP
from pprint import pprint

class Test_TestNLP(unittest.TestCase):
    # test get_keywords
    def test_get_keywords(self):
        data = [
            {
                'url': 'https://www.usatoday.com/story/news/nation/2021/11/10/atmospheric-river-wallop-pacific-northwest/6370849001/',
                'heading': 'Atmospheric river to wallop Pacific Northwest',
                'description': "Another round of\xa0heavy, potentially flooding rain is forecast across portions of the Pacific Northwest on Thursday and into Friday thanks to an atmospheric river that's forecast to hit the region. The heavy rain will create areas of flash flooding, and\xa0urban areas, roads and small streams will be the most vulnerable, primarily in Washington and Oregon, the National Weather Service said.\xa0 The storm could drop nearly a month’s worth of rain in some areas.\xa0"
            },
            {
                'url': 'https://www.nbcnews.com/news/us-news/ability-force-recalls-fda-can-only-warn-consumers-benzene-hand-sanitiz-rcna4585',
                'heading': 'Without ability to force recalls, FDA can only warn consumers about benzene in hand sanitizers',
                'description': '“The toxicity of benzene has been known for over 120 years. It’s directly linked with causing leukemia in humans,” said the CEO of a lab that found the contamination. When Kayla Ridgely, a nurse in Queen Creek, Arizona, stumbled across bottles of hand sanitizer on sale for 99 cents at her local Walmart, it seemed like a gold mine. It was early in the pandemic, when cleaning products were in short supply, and the sanitizer was marketed as safe and plant-based, with a brand name that emphasized that messaging: Artnaturals, a company best known for its essential oils and hair products. But earlier this year, Ridgely came across a study showing that the brand of hand sanitizer she had been using throughout the pandemic had sold bottles that tested positive for benzene, a solvent made from petroleum that is not allowed to be used in consumer products because it is carcinogenic.\xa0 Valisure, the lab that made findings about benzene in samples of Artnaturals sanitizer and other brands, had submitted a citizen petition in March asking the FDA to take action on Artnaturals and other hand sanitizer products. It also offered on its website to test more samples free of charge to anyone else who would send their sanitizer in.\xa0 So Ridgely submitted hers and received results in April that it was contaminated with benzene at levels of 13 parts per million — thousands of times above the EPA’s benzene limits of 5 parts per billion in drinking water, and more than six times above the FDA’s temporary guidance during the pandemic allowing trace amounts of benzene in over-the-counter drugs. “The toxicity of benzene has been known for over 120 years. It’s directly linked with causing leukemia in humans. It’s a group one carcinogen, it’s at the top of the FDA list of chemicals not to use in manufacturing,” David Light, the CEO of the Valisure lab, said.\xa0 His lab’s research into hand sanitizers was the start of a disturbing trend. Over the past year, Valisure tests have found benzene in everyday consumer products like sunscreen, antifungal sprays and most recently, antiperspirant sprays. According to a Nov. 3 petition that Valisure sent to the FDA, some samples of Old Spice antiperspirant had levels of benzene at 17 parts per million. The brand’s parent company P&G did not respond to NBC News’ request for comment. Consumers are left largely in the dark about the scope of the problem. In the case of hand sanitizer, regulators and industry have been slow to act, according to consumers and experts.\xa0'
            },
            {
                'url': 'https://www.nytimes.com/2021/11/10/climate/climate-cop26-glasgow.html',
                'heading': 'China and the United States Join in Seeking Emissions Cuts',
                'description': 'As nearly 200 nations struggle over global climate negotiations, the world’s two biggest polluters sign an agreement, but it was short on details. GLASGOW — The United States and China announced a joint agreement Wednesday to “enhance ambition” on climate change, saying they would work together to do more to cut emissions this decade while China committed for the first time to reduce methane, a potent greenhouse gas. The pact between the world’s two biggest polluters came as a surprise to the thousands of attendees gathered here for a United Nations climate summit. China and the United States, rivals that face growing tensions over trade, human rights and other issues, spoke as allies in the fight to keep global warming to relatively safe levels.  “We both see the challenge of climate change is existential and a severe one,” said Xie Zhenhua, China’s climate change envoy. “As two major powers in the world, China and the United States, we need to take our due responsibility and work together and work with others in the spirit of cooperation to address climate change.” John Kerry, the U.S. special envoy for climate, followed the remarks from Mr. Xie with an assessment of his own. “The U.S. and China have no shortage of differences,” said Mr. Kerry, a former secretary of state with a long history of negotiating with the Chinese. “But on climate, cooperation is the only way to get this job done.” Still, the joint agreement was short on specifics. It did not extract a new timetable from China under which the country would ratchet down emissions, nor did China set a ceiling for how high its carbon dioxide and other greenhouse gases would reach before they started to fall. China agreed to “phase down” coal, the dirtiest fossil fuel, starting in 2026, but did not specify by how much or over what period of time. The announcement from China and the United States came on the same day that summit organizers issued an initial draft of a new global agreement to fight climate change that called on countries to “revisit and strengthen” by the end of 2022 plans for cutting greenhouse gas emissions and to “accelerate the phasing-out of coal and subsidies for fossil fuels.” The language on coal and government fossil fuel subsidies would be a first for a U.N. climate agreement if it stays in the final version. Yet many countries and environmentalists said the rest of the document was still too vague on crucial details like what sorts of financial aid richer nations should provide poorer ones struggling with the costs of climate disasters and adaptation. The draft “is not the decisive language that this moment calls for,” said Aubrey Webson, chairman of the Alliance of Small Island States, a group of countries that are among those most threatened by climate change. Scientists have said that nations need to cut global emissions from fossil fuels roughly in half this decade to keep average global temperatures from rising beyond 1.5 degrees Celsius, or 2.7 degrees Fahrenheit, compared with preindustrial levels. Beyond that threshold, the risks of deadly heat waves, droughts, wildfires, floods and species extinction grow considerably. The planet has already warmed 1.1 degrees Celsius.'
            }
        ]

        expected_keywords = [
            {
                'atmospheric',
                'northwest',
                'oregon',
                'pacific',
                'river',
                'the national weather service',
                'wallop',
                'washington'
            },
            {
                'ability',
                'arizona',
                'benzene',
                'consumer',
                'epa',
                'fda',
                'force',
                'hand',
                'nbc news’',
                'p&g',
                'recall',
                'sanitizer',
                'warn'
            },
            {
                '2022',
                'aubrey webson',
                'china',
                'cut',
                'emission',
                'john kerry',
                'join',
                'kerry',
                'seek',
                'states',
                'the united states',
                'u.n.',
                'u.s.',
                'united',
                'united nations',
                'xie',
                'xie zhenhua'
            }
        ]
        keywords = NLP(data).get_keywords()
        print("keywords:")
        pprint(keywords)
        self.assertEqual(keywords, expected_keywords)
