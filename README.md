# piloadcell
Python code for raspberry pi, load cell and hx711 converter

Includes code to generate tab delimited averaged readings sampled every (e.g.) minute so we can evaluate drift and figure out
how to compensate for temperature. Also includes a flask server to get plots of current accumulated data from the output
of the sampler process.

Background: Load cells suck. The beekeepers have dropped them from the openhivescale project, preferring a much more
mechanical system based on a foundary scale design. Load cells suffer from drift and temperature changes, but
cheap ones can be had for cheap - so little investment for fun. Being a data scientist means I want to know how badly
they suck...so I grabbed some cheap 10kg load cells and hx711 converter boards from eGay, knowing I was in for a rough ride.
Turns out they're not that bad...

Lessons so far:

* Using these cheapo hx711, dropping the hx711 supply from 5v to 3.3v resulted in huge gains in stability. Go figure. Both are within
the datasheet specs.

* Using the hx711py read_average function with 10 samples seems to give reasonable estimates - trims the top and bottom values.

* Similarly, the code to manage readings allows the hx711 to sleep most of the time to minimise on board thermal effects. Seems also to
improve stability a lot.

* Getting matplotlib to plot a pandas timestamp on the x axis was a frustrating exercise - at least partly because
I'm using the raspbian versions of everything to make the project easier to test.
