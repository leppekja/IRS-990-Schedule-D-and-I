# 990-DAFs
Code for analyzing Donor Advised Funds 

## Overview

Donor Advised Funds (DAF) are some of the largest nonprofit organizations in the world, distributing billions of dollars to NGOs each year. This project attempts to map and analyze the flow of these funds from DAFs to NGOs. DAFs are required to report any cumulative grants greater than $5,000 in the IRS 990 Form Schedule I. 


### Step 1 - INCOMPLETE

Code for reading XML [Schedule I](https://www.irs.gov/pub/irs-pdf/f990si.pdf) forms. Files are available in XML format from multiple locations, including AWS (easily accessible through [open990.org](https://www.open990.org/org/680480736/network-for-good-inc/)). Need to collect, for each organization, the name, address, EIN, IRS organization type e.g. 501(c)(3), and amount of grant, with a indicator for which DAF the funds were distributed through. Will read this data into a Pandas Dataframe for analysis. 