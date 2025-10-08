# A dataset from ten disasters for studying location descriptions and training AI models

### Overall description
Location information is highly important during a natural disaster for reaching victims and coordinating response and relief efforts. In recent years, people increasingly use social media to post messages during a disaster, and describe the locations of victims, damages, difficult situations, and relief resources. Many of these location descriptions are in the forms of detailed and multi-entity descriptions, such as door number addresses, road intersections, and highway exits. Currently, there is limited availability of datasets containing these detailed location descriptions, which hinders their understanding and automatic extraction. This paper fills this gap by providing a dataset that contains labeled location descriptions from ten disasters in the United States and in five disaster types: hurricanes, floods, wildfires, tornados, and winter storms. The social media messages containing location descriptions are collected from the platform Twitter/X, and we describe the collection, labeling, and validation of this dataset. This dataset can be used for studying the ways people describe locations under disaster contexts and for training AI models to extract these important locations.


### Data description
This dataset contains 7,149 tweets related the 10 disasters. The 10 disasters include: *2017 Hurricane Harvey, 2018 California Camp Fire, 2020 Easter Tornado Outbreak, 2021 Texas Winter Storm, 2021 Kentucky Tornado, 2022 St. Louis Flooding, 2022 Hurricane Ian, 2022 Buffalo Blizzard, 2022 California Flooding, and 2023 Hawaii Firestorm*. It was collaboratively annotated by the University at Buffalo and the Geocove company. The annotators include disaster experts, GIS professionals, and GIS graduates. The annotation tool is [GALLOC](https://github.com/geoai-lab/GALLOC). 

The dataset can be downloaded at the link: https://geoai.geog.buffalo.edu/VariousResources/DisasterLocDesc_Data_Public.zip. Note that the files contain only annotations and do not include the original text of tweets. The version containing the original text is available from the corresponding author upon reasonable request.




### Other files
The file "DisasterLocDesc_Annotation_Guideline.pdf" provides the guidelines followed by annotators for message annotation. The four Python scripts (.py) were used to preprocess the original tweets and  annotations:
* Data_Collection.py: collect disaster-related tweets using the Twitter/X API;
* Data_Preprocessing.py: preprocess tweets through length filtering, deduplication, and location description–based filtering;
* Data_Random_Selection.py: randomly sample tweets from the preprocessed data;
* Annotations_Compare.py: compare location description annotations from annotators against the ground truth;

### Authors
* **Kai Sun** - *GeoAI Lab* - Email: ksun4@buffalo.edu
* **Yingjie Hu** - *GeoAI Lab* - Email: yhu42@buffalo.edu



### Reference
If you use the data or code from this repository, we will really appreciate if you can cite our paper:

Kai Sun and Yingjie Hu. 2025. How do people describe locations during a natural disaster: a dataset with labeled location descriptions from ten disasters.
