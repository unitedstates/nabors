Bill Numbers for Early American Statutes
========================================

This is a project by [Joshua Tauberer](http://razor.occams.info) ([@JoshData](https://www.github.com/JoshData)) to digitize Eugene Nabors's [Legislative Reference Checklist: The Key to Legislative Histories from 1789-1903](http://www.worldcat.org/title/legislative-reference-checklist-the-key-to-legislative-histories-from-1789-1903/oclc/8806745), published in 1982.

What this is
------------

From the founding of the United States through 1903, the official compilation of Congress's enacted statutes omitted the identifying numbers of the bills that were enacted, making it difficult now to see the legislative history of these early laws.

In 1982 Eugene Nabors published [Legislative Reference Checklist: The Key to Legislative Histories from 1789-1903](http://www.worldcat.org/title/legislative-reference-checklist-the-key-to-legislative-histories-from-1789-1903/oclc/8806745), in which he meticulously researched which bills corresponded to each of the approximately 15,000 statutes enacted through 1903. His research provides a crucial link between our early statutory law and the legislative histories of those laws.

His book is a 428-page table that lists for each law the:

* Slip law citation (public law or resolution chapter and number).
* Statutes at Large citation (volume and page range).
* Date of enactment.
* Bill number.

The book's full citation is Eugene Nabors. 1982. Legislative Reference Checklist: The Key to Legislative Histories from 1789-1903. Fred B. Rothman & Co. Littleton, Colorado. ISBN 0-8377-0908-3.

The book has a copyright notice at the start (listing Nabors as the copyright holder). I attempted to locate Nabors or his descendants to obtain permission for this project but was unable to locate anyone. Facts cannot be copyright, however, so I proceeded ahead with this project. I'd be glad to discuss this project further with the copyright holder.

Details
-------

[table.csv](table.csv) lists bills and joint resolutions which became law from the 1st Congress (1789) through the 57th Congress (1903). The columns are:

* `nabors-page`: The page number on which this row of information occurs in Nabors's book.

* `congress`: The number of the Congress in which the bill was introduced.

* `slip-chapter` and `slip-number`: The public law or public resolution chapter and number for citation as a slip law. Chapter numbers were assigned chronologically to bills and joint resolutions as they were enacted. Since private laws were omitted from the table and the table is ordered by the Statutes at Large, in which resolutions follow bills, chapter numbers skip around.

* `stat-volume`, `stat-page-start`, and `stat-page-end`: The volume of the Statutes at Large and the page range that this bill or resolution appears at, for forming a "X Stat Y" citation.

* `date`: The date of enactment of the statute.

* `bill-type` and `bill-number`: The bill or resolution number corresponding to the statute. `bill-type` is one of `HR` or `S` (for bills) or `HJRES` or `SJRES` (for resolutions). (Note that from the 29th Congress, 2nd session through the 55th (House) and 56th (Senate) Congresses these were denoted simply H. Res. and S.Res., but they were in fact joint resolutions.) There are a number of oddities related to bill numbering --- see below. 

* `has-note`: Whether Nabors marked the row with an asterisk (see Nabors's [Notes](pages/notes.md)).

Files inside
------------

In this repository you'll find a CSV file containing the correspondence table between bills and statutes:

* [table.csv](table.csv) (pages 1-428) (IN PROGRESS)

And OCR'd text for:

* [title page](pages/title-page.md)
* [copyright page](pages/copyright-page.md)
* [Nabors's dedication](pages/dedication-page.md)
* [Foreward by Ellen P. Mahar and J. S. Ellenberger](pages/foreward.md) (pages vii-viii)
* [Acknowledgements](pages/acknowledgements.md) (page ix)
* [Introduction](pages/introduction.md) (pages xi-xiii)
* [User's Guide](pages/users-guide.md) (page xv)
* [Notes](pages/notes.md) (pages 429-437)
* [Bibliography](pages/bibliography.md) (pages 439-440)

(I cleaned up the text and formatted it as Markdown.)

Data oddities
-------------

Chapter numbers were assigned chronologically to laws, including both bills and joint resolutions. They restart each session. So-called private laws were omitted from the table so chapter numbers may skip.

Some bill numbers are strange:

* From the 1st through 14th Congress, it is not clear how the House and Senate numbered its bills.

* Starting with the 15th Congress, the House numbered bills in the usual way: resetting numbering at the end of each Congress. Until the 30th Congress, Senate bill numbering reset with each session.

* In the 3rd Congress, 1st session, two bills were named "S. 16" (both were enacted and appear in this table). In the 10th Congress, 1st session, "H.R. 26" and "S. 1" each appear twice in the House Journal (the latter as "S. 1a" and "S. 1b"). It is not clear from this table which were enacted.

* In the 13th Congress, 2nd session, "HR 197" here is "HR 197b" in the House Journal. In the 15th Congress, 1st session, "S. 14" here is "S. 14 2nd" in the House Journal. In the 16th Congress, 1st session, "HR 145" here is "HR 145b" in the House Journal. In the 19th Congress, 2nd session, "S. 53" and "S. 52" here are "S. 53a" and "S. 52b" in the House Journal. In the 22nd Congress, 2nd session, "HJR 15" here is "HJR 15b" in the House Journal.

* In the 38th Congress, 1st session, there is a bill "HR 14½".

* In the 38th Congress, 2nd session, "H. Res. 170" was printed along with the public acts in the Statutes at Large. This may have been an actual House simple resolution that, somehow, was enacted as if it were a House joint resolution.


How the files were produced
---------------------------

I had Nabors's book scanned, and then I OCR'd the resulting PDF:

	# Turn the 21 MB PDF into 18 GB of .ppm and .pbm files. Each page
	# decomposes into three image files. I don't know why exactly but
	# I'm sure it has to do with efficient compression.
	pdfimages -j nabors.pdf image

	# For whatever reason, just the monochrome "mask" for each page has
	# the actual text of the book. Make a table mapping page numbers to
	# image numbers. Unfortunately while pdfimages zero-pads image numbers
	# pdfimages doesn't, so force some zero-padding with a quick Perl
	# script.
	pdfimages -list nabors.pdf \
		| grep mask \
		| perl -n -e '@_ = split(/ +/); printf "%03d %03d\n", $_[1], $_[2];' \
		> page-images.txt 

	# Make thumbnails of all of the pages.
	cat page-images.txt | bash -c 'while read PAGE IMG; do convert image-$IMG.pbm -negate -resize 500 -depth 2 page-$PAGE.png; done'

	# Run tesseract on each page.
	# This generates "page-###.txt" files.
	# psm=6 means "Assume a single uniform block of text." It roughly
	# preserves the layout of the page, which we'll need to parse.
	cat page-images.txt | bash -c 'while read PAGE IMG; do tesseract image-$IMG.pbm -psm 6 page-$PAGE; done'

	# Split and name pages. (Blank pages and the table of contents are omitted.)
	cat page-005.txt > title-page.md
	cat page-006.txt > copyright-page.md
	cat page-007.txt > dedication-page.md
	cat page-{011..012}.txt > foreward.md
	cat page-013.txt  > acknowledgements.md
	cat page-{015..017}.txt > introduction.md
	cat page-019.txt > users-guide.md
	cat page-{449..458}.txt > notes.md
	cat page-{459..460}.txt > bibliography.md

The pages saved as Markdown were manually reviewed/corrected by me.

I then re-OCR'd the text restricting tesseract's output to a small set of characters to try to get more consistent output for the table, and ran a scraping script to turn the raw text into CSV format:

	cat page-images.txt | bash -c 'while read PAGE IMG; do echo $PAGE; tesseract $IMG.pbm -psm 6 page-$PAGE -c tessedit_char_whitelist=0123456789-HSJRes./*PUBCACTSRSUTNSTHCNGR; done'

	python3 parse_table.py page- > table.csv

