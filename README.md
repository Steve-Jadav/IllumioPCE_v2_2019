# IllumioPCE_v2_2019
This repository contains my approach to Illumio's take-home coding assignment, which is a component of their interview process.


Create a virutal environment and activate source

    virtualenv venv
    source venv/bin/activate
    
Install the required packages for this assignment by typing the following:
   
    pip3 install -r requirements.txt
    
Hello, my name is Steve, and this is my solution for the Illumio coding challenge!

Given that there can be a huge number of rules for the program to search through, I immediately cut-off the idea of a sequential search. The next idea, that came to mind was by somehow using a Bloom Filter data structure. A bloom filter is a space-efficient probabilistic data structure that is used to test whether an element is a member of a set. In our particular case, it means that using a bloom filter, the program will be able to search through millions of rules extremely quickly. But, an important thing to understand is that it is a probabilistic data structure, that means, there are chances that it might not match a rule and still say that it did. This is not a desirable case because it means accepting a packet which is not supposed to be accepted. Although, bloom filter works with a lot of use cases, chances are, that it'll make the Firewall vulnerable.

So, in limited time constraints, I thought of proceeding with Binary Search. The idea was to first sort a Pandas DataFrame based on the start_range of a given port range. The binary search will be performed based on the start_range of the port number. This approach eliminates a lot of rules which are not required to be checked. However, implementing a binary search using a column can be quite tricky. As a result, I could not complete the implementation in the required time. However, I already designed the program structure and test cases at the start of the challenge, which spared me some time, but still wasn't enough. Over the years, this is the first time, I have ever attempted to implement binary search on a data structure, which is complex than a simple array. Nonetheless, I still feel that I was extremely close to the solution.

If I had more time, I would've managed to complete the binary search implementation. A simple sequential search through the input rules, would have been simpler but equally costly, in terms of the time required to match a rule. Hence, that would not have been a good approach, even if it was guaranteed to work.

I have tried to make the code as neat and readable as possible. I hope you enjoy looking through my solution as much as I enjoyed working through it.

Regarding the teams, I've always been more inclined towards working with data. Hence, my preference would be to work with the Data team.

Thanks,

Steve 
