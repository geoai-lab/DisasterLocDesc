# A dataset from ten disasters for studying location descriptions and training AI models

### Overall description
Location information is highly important during a natural disaster for reaching victims and coordinating response and relief efforts. In recent years, people increasingly use social media to post messages during a disaster, and describe the locations of victims, damages, difficult situations, and relief resources. Many of these location descriptions are in the forms of detailed and multi-entity descriptions, such as door number addresses, road intersections, and highway exits. Currently, there is limited availability of datasets containing these detailed location descriptions, which hinders their understanding and automatic extraction. This paper fills this gap by providing a dataset that contains labeled location descriptions from ten disasters in the United States and in five disaster types: hurricanes, floods, wildfires, tornados, and winter storms. The messages containing location descriptions are collected from the social media platform Twitter/X, and we describe the collection, labeling, and validation of this dataset. This dataset can be used for studying the ways people describe locations under disaster contexts and for training AI models to extract these important locations.


### Data description
This dataset contains 7,149 tweets from 10 disasters across five disaster types. The 10 disasters are:
* Hurricanes: 2017 Hurricane Harvey, 2022 Hurricane Ian
* Wildfires: 2018 California Camp Fire, 2023 Hawaii Firestorm
* Floods: 2022 St. Louis Floods, 2022 California Floods
* Tornados: 2020 Easter Tornado Outbreak, 2021 Kentucky Tornado
* Winter storms: 2021 Texas Winter Storm, 2022 Buffalo Blizzard

This dataset was collaboratively annotated by the University at Buffalo and a professional GIS company that specializes in disaster management. The annotators are disaster management and GIS experts. The annotation tool used is [GALLOC](https://github.com/geoai-lab/GALLOC). 

The public version of this annotated dataset can be downloaded at the link: https://geoai.geog.buffalo.edu/VariousResources/DisasterLocDesc_Data_Public.zip. Following the data sharing policy of X/Twitter, the public version does not contain full tweets but contains tweet ID and annotations. A private version of this dataset containing full tweets is available upon email requests to the first and corresponding authors. Due to the sensitive nature of this dataset (e.g., locations of victims during a disaster), we ask interested researchers to complete a responsible conduct of research training course, such as the one from the Collaborative Institutional Training Initiative (CITI) Program, and show a course completion certificate when requesting this dataset.




### Other files
The file "DisasterLocDesc_Annotation_Guideline.pdf" provides the guidelines for human annotators to do the annotation work. The four Python scripts (.py) contain the code used for collecting and preparing tweets, as well as for comparing annotations:
* Data_Collection.py: The code for collectomg disaster-related tweets using the Twitter/X API;
* Data_Preprocessing.py: The code for preprocessing and preparing tweets by applying three filters to the collected data including a tweet-length filter, a deduplication filter, and a location-term filter;
* Data_Random_Selection.py: The code for randomly sampling tweets from the preprocessed data;
* Annotations_Compare.py: The code for comparing location description annotations with the ground truth;

### Authors
* **Kai Sun** - *GeoAI Lab* - Email: kaisun@cuhk.edu.hk
* **Yingjie Hu** - *GeoAI Lab* - Email: yhu42@buffalo.edu



### Reference
If you use the data or code from this repository, we will really appreciate if you can cite our paper:

Kai Sun, Yingjie Hu, and Kenneth Joseph. 2025. A dataset from ten disasters for studying location descriptions and training AI models.
