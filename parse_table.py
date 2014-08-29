# This Python 3 script parses the tesseract-OCR'd text
# from the table in the Nabors book and generates a CSV
# file.

import sys, re, csv

def main():
	w = csv.writer(sys.stdout)
	w.writerow([
		"nabors-page",
		"congress",
		"slip-chapter", "slip-number",
		"stat-volume", "stat-page-start", "stat-page-end",
		"date",
		"bill-type", "bill-number",
		"has-note" ])

	congress = None

	for page in range(21, 448+1):
		for line in open("%s%03d.txt" % (sys.argv[1], page)):
			line = line.strip()
			if line == "": continue

			if re.match("^\d+$", line):
				# page number
				continue

			line = line.replace(".", "")

			if len(line) < 15:
				continue

			m = re.search("[T1]H1?[RHB823S4]J? (.*) [C0].*(SS|88)$", line, re.I)
			if m:
				if m.group(1) in congress_numbers():
					congress = congress_numbers()[m.group(1)]
					continue

			# Headers are garbled because we restricted the output
			# to a small subset of unicode characters.
			if re.search(r'[A-Z]{4}', line):
				continue
			if re.search(r'\d{8}', line):
				continue
			if re.search(r'[A-Z]\S{3}[A-Z]', line):
				continue
			if re.search(r'P[3e82]1?[9s][e3689]', line):
				continue

			has_note = "*" if ("*" in line) else ""
			line2 = line
			line2 = line2.replace("*", "-")
			line2 = line2.replace("  ", " ")
			line2 = re.sub(" - |- | -", " ", line2)
			m = re.match("\s*(\d+) (\d+) (\d+) (?:1 )?(\d+)(?:-(\d+))? (?:1 )?([\d\-]+) (HR|[S583]|HJR|[S583]JR|(?:H|[S583]) ?R(?:es|.* )) ?(\d+)", line2, re.I)
			if m:
				slip_chapter, slip_number, stat_volume, stat_page_start, stat_page_end, date, bill_type, bill_number \
					= m.groups()

				try:
					month, day, year = [int(x) for x in date.split("-")]
					if page <= 40:
						year += 1700
					elif page <= 422:
						year += 1800
					else:
						year += 1900
					date = "%04d-%02d-%02d" % (year, month, day)

					bill_type = bill_type.strip()
					if re.match("^[H8]R$", bill_type):
						bill_type = "HR"
					elif re.match("^[S583s]$", bill_type):
						bill_type = "S"
					elif re.match("^HJR$", bill_type):
						bill_type = "HJRES"
					elif re.match("^[S583s]JR$", bill_type):
						bill_type = "SJRES"
					elif re.match("^H ?Re[sS]$", bill_type):
						bill_type = "HJRES"
					elif re.match("^[S583s] ?R(e[sS]?)?$", bill_type):
						bill_type = "SJRES"
					else:
						raise ValueError()

					w.writerow([page-20, congress, slip_chapter, slip_number, stat_volume, stat_page_start, stat_page_end, date, bill_type, bill_number, has_note])
					continue
				except:
					pass

			w.writerow([page-20, congress] + line.split(" ") + [has_note, "ERROR"])

def congress_numbers():
	return {
	'R1RST': 1,
	'P1RST': 1,
	'H1RST': 1,
	'SBCCNB': 2,
	'SBCGNB': 2,
	'SR00N0': 2,
	'TH1RB': 3,
	'TH1R0': 3,
	'R0URTH': 4,
	'PCURTH': 4,
	'518TH': 5,
	'R1RTH': 5,
	'H1HTH': 5,
	'P1PTH': 5,
	'PTPTH': 5,
	'P11P1TH': 5,
	'S1RTH': 6,
	'S1HTH': 6,
	'SRHHNTH': 7,
	'SBR/BNTH': 7,
	'SRHRNTH': 7,
	'H1GHTH': 8,
	'R1GHTH': 8,
	'B1GHTH': 8,
	'N1NTH': 9,
	'TBNTH': 10,
	'THNTH': 10,
	'RRRHRNTH': 11,
	'HHBHHNTH': 11,
	'2121/3NTH': 12,
	'RRRHHNTH': 12,
	'THRRRTH': 13,
	'THHHRTH': 13,
	'THRHPTH': 13,
	'TNRRRTH': 13,
	'TNRJJPTH': 13,
	'TH1RTBBNTH': 13,
	'TH1RT813NTH': 13,
	'TH1RTRBNTH': 13,
	'TH1RTRHNTH': 13,
	'TH1RTRRNTH': 13,
	'TH1RT13BNTH': 13,
	'R0URTHRNTH': 14,
	'H0URTHHNTH': 14,
	'RGURTHHNTH': 14,
	'P0URTHHNTH': 14,
	'H0URTHBNTH': 14,
	'P1RTHHNTH': 15,
	'P1PTRBNTH': 15,
	'818TRSNTH': 15,
	'818T8BNTH': 15,
	'R1RTRRNTH': 15,
	'R1RTHRNTH': 15,
	'S1RTRHNTH': 16,
	'S1RTHHNTH': 16,
	'S1RTBHNTH': 16,
	'S1HTRRNTH': 16,
	'SHHHNTHRNTH': 17,
	'SRHRNTHRNTH': 17,
	'SHHHNTRRNTH': 17,
	'SR7HNTRRNTH': 17,
	'SHHRNTRHNTH': 17,
	'SHHRNTHHNTH': 17,
	'B1GHTBBNTH': 18,
	'B1GHTRRNTH': 18,
	'81GHTJS3NTH': 18,
	'B1GHT8RNTH': 18,
	'H1GHTHHNTH': 19,
	'R1GHTRRNTH': 19,
	'N1NHTHRNTH': 19,
	'N1NRTRHNTH': 19,
	'N1NHTHHNTH': 19,
	'N1NBTRRNTH': 19,
	'N1NBTBBNTH': 19,
	'THHNT1HTH': 20,
	'THBNT1HTH': 20,
	'THRNT1RTH': 20,
	'TUU3NT13TH': 20,
	'T1NBNT1BTH': 20,
	'THHNTH-P1RST': 21,
	'THHNTH-H1RST': 21,
	'T0BNT3-01RST': 21,
	'THRNTH-R1RST': 21,
	'THHNT1-R1RST': 21,
	'THBNTH-R1RST': 21,
	'THRNT7-SRC0NB': 22,
	'THHNTH-SHC0NB': 22,
	'THBNT1-SRC0NB': 22,
	'T0BNT1-S8C0NB': 22,
	'T0BNT1-SBC0NB': 22,
	'THBNTH-SHC0NB': 22,
	'THRNTH-SRC0NB': 22,
	'THHNTH-SRC0NB': 22,
	'THRNTR-TH1R0': 23,
	'THRNTH-TH1RB': 23,
	'T08NT1-TH1RB': 23,
	'T0BNT1-TH1RB': 23,
	'THHNT8-P0URTH': 24,
	'THRNTR-R0URTH': 24,
	'T48NT1-70URTH': 24,
	'T43NT1-P0URTH': 24,
	'THHNTR-R0URTH': 24,
	'T0BNT1-P0URTH': 24,
	'T0HNT1-P0URTH': 24,
	'T0BNT1-818TH': 25,
	'THRNTH-P1PTH': 25,
	'THHNTH-R1RTH': 25,
	'T03NT1-818TH': 25,
	'T08NT1-818TH': 25,
	'THRNTH-R1RTH': 25,
	'TN2NT1-P1PTH': 25,
	'T62NT1-51PTH': 25,
	'THRNTR-S1RTH': 26,
	'THHNTH-S1RTH': 26,
	'THHNT1-S1RTH': 26,
	'THRNT8-SRHRNTH': 27,
	'THRNTH-SHHRNTH': 27,
	'THRNTH-SRHRNTH': 27,
	'THHNTH-SRHHNTH': 27,
	'THHNT7-SHHRNTH': 27,
	'THHNT8-SHHHNTH': 27,
	'THHNTR-SRHRNTH': 27,
	'THHNT1-SHHRNTH': 27,
	'THHNT1-SRHHNTH': 27,
	'THHNTH-H1GHTH': 28,
	'THHNTH-R1GHTH': 28,
	'THBNTH-H1GHTH': 28,
	'TUUBNT1-131GHTH': 29,
	'THRNT1-B1GHTH': 29,
	'T00NT7-01GHTH': 29,
	'T7BNT7-B1GHTH': 29,
	'THHNTH-N1NTH': 29,
	'THBNTH-NRNTH': 29,
	'THRNTH-N1NTH': 29,
	'TH1RT1HTH': 30,
	'TH1RT1BTH': 30,
	'TH1RT1RTH': 30,
	'TH1RT1-P1RST': 31,
	'TH1RT7-R1RST': 31,
	'TH1RTR-P1RST': 31,
	'TH1RTH-R1RST': 31,
	'TH1RT1-SHC0NB': 32,
	'TH1RT1-SHC0N0': 32,
	'TH1RT7-SHC0NB': 32,
	'TH1RT1-SRC0NB': 32,
	'TH1RTR-TH1RB': 33,
	'TH1RT1-TH1RB': 33,
	'TH1RT2-TH1RB': 33,
	'TH1RT1-P0URTH': 34,
	'TH1RT1-H0URTH': 34,
	'TH1RT1-R0URTH': 34,
	'TH1RT1-R1RTH': 35,
	'TH1RT1-R1HTH': 35,
	'TH1RT1-H1PTH': 35,
	'TH1RTR-R1RTH': 35,
	'TH1RT1-S1RTH': 36,
	'TH1RTH-S1HTH': 36,
	'TH1RT1-S1HTH': 36,
	'TH1RTH-SHHHNTH': 37,
	'TH1RT1-SHHBNTH': 37,
	'TH1RT1-SRHRNTH': 37,
	'TH1RT1-SHHRNTH': 37,
	'TH1RT7-SBHBNTH': 37,
	'TH1RT1-SBHBNTH': 37,
	'TH1RT1-SBHHNTH': 37,
	'TH1RT1-SB7BNTH': 37,
	'TH1RT1-SHHHNTH': 37,
	'TH1RT7-SH7HNTH': 37,
	'TH1RT1-S38BNTH': 37,
	'TH1RTH-B1GHTH': 38,
	'TH1RTH-H1GHTH': 38,
	'TH1RTH-R1GHTH': 38,
	'TH1RT1-H1GHTH': 38,
	'TH1RT1-B1GHTH': 38,
	'TH1RT1-R1GHTH': 38,
	'TH1RTH-N1NTH': 39,
	'TH1RT1-N1NTH': 39,
	'TH1RTR-N1NTH': 39,
	'R0RT1RTH': 40,
	'H0RT1RTH': 40,
	'P0RT1HTH': 40,
	'P0RT1RTH': 40,
	'P0RT1BTH': 40,
	'H0RT1HTH': 40,
	'H0RT1BTH': 40,
	'R0RT1-R1RST': 41,
	'P0RT1-R1RST': 41,
	'P0RT1-P1RST': 41,
	'R0RT8-R1RST': 41,
	'H0RT1-P1RST': 41,
	'P0RT1-H1RST': 41,
	'P0RTH-P1RST': 41,
	'R0RTH-P1RST': 41,
	'H0RT1-H1RST': 41,
	'R0RT1-SRC0NB': 42,
	'P0RT1-SRC0NB': 42,
	'H0RT1-SBC0NB': 42,
	'R0RT1-SB00N0': 42,
	'R0RTH-SBC0NB': 42,
	'80RT1-SHCCNB': 42,
	'P0RT1-SHCCNB': 42,
	'H0RT1-SRC0NB': 42,
	'R0RTH-SHC0NB': 42,
	'P0RT8-SBC0NB': 42,
	'P0RTR-SBC0N0': 42,
	'P0RT1-SBC0N0': 42,
	'P0RT1-SBC0NB': 42,
	'P0RTH-TH1RB': 43,
	'R0RT1-TH1R0': 43,
	'P0RT1-TH1RB': 43,
	'H0RT1-TH1RB': 43,
	'R0RT1-TH1RB': 43,
	'H0RT1-H0URTH': 44,
	'HCRTH-HCURTH': 44,
	'RCRTH-PCURTH': 44,
	'HCRTH-HGURTH': 44,
	'P0RTH-P0URTH': 44,
	'P0RT1-60URTH': 44,
	'R0RT1-P0URTH': 44,
	'R0RT1-R0URTH': 44,
	'P0RT1-P1PTH': 45,
	'P0RT1-H1PTH': 45,
	'R0RT1-H1RTH': 45,
	'PCRT1-P1PTH': 45,
	'P0RTH-P1PTH': 45,
	'H0RT1-R1RTH': 45,
	'R0RT1-R1RTH': 45,
	'H0RTH-R1RTH': 45,
	'H0RT1-P1RTH': 45,
	'H0RT1-31HTH': 46,
	'H0RT1-81HTH': 46,
	'P0RT1-S1HTH': 46,
	'P0RTH-S1HTH': 46,
	'R0RT1-S1HTH': 46,
	'H0RT1-S1HTH': 46,
	'H0RT1-SHHHNTH': 47,
	'H0RTH-SHHHNTH': 47,
	'H0RT1-SBHHNTH': 47,
	'P0RT1-SRHRNTH': 47,
	'HCRTH-SRHHNTH': 47,
	'PCRTH-SHHHNTH': 47,
	'R0RT1-SHHHNTH': 47,
	'HURTH-SHHHNTH': 47,
	'P0RT1-S84BNTH': 47,
	'P0RTH-SBHBNTH': 47,
	'PCRTH-SBHBNTH': 47,
	'PGRTH-SBHBNTH': 47,
	'P0RT7-B1GHTH': 48,
	'R0RT1-R1GHTH': 48,
	'H0RTH-H1GHTH': 48,
	'P0RT1-R1GHTH': 48,
	'80RT8-B1GHTH': 48,
	'R0RTH-R1GHTH': 48,
	'H0RT1-H1GHTH': 48,
	'R0RT7-R1GHTH': 48,
	'R0RT1-H1GHTH': 48,
	'H0RTH-B1GHTH': 48,
	'P0RT1-N1NTH': 49,
	'R0RT1-N1NTH': 49,
	'H0RT1-N1NTH': 49,
	'P0RTH-N1NTH': 49,
	'R0RTH-N1NTH': 49,
	'H0RTH-N1NTH': 49,
	'R1RT1RTH': 50,
	'H11TT1BTH': 50,
	'R1HT1HTH': 50,
	'P1PT1HTH': 50,
	'H1HT1HTH': 50,
	'H1RT1HTH': 50,
	'H1HT1BTH': 50,
	'P1HT1HTH': 50,
	'R1RT1BTH': 50,
	'PJTTUBTH': 50,
	'P1PT1-P1RST': 51,
	'P1PT7-P1RST': 51,
	'PTHTH-HTRST': 51,
	'R1RT1-R1RST': 51,
	'H1HT1-H1R5T': 51,
	'H1HT1-H1RST': 51,
	'P1PTH-P1RST': 51,
	'H1HTH-H1RST': 51,
	'H1HTH-P1RST': 51,
	'H1RT1-H1RST': 51,
	'P1PTH-H1RST': 51,
	'H1HT1-R1R8T': 51,
	'H1HTH-SHC0NB': 52,
	'R1RT1-SH00N0': 52,
	'R1RT1-SHC0N0': 52,
	'P1PT1-SRC0NB': 52,
	'R1RT1-SHC0NB': 52,
	'H1HTH-SBC0NB': 52,
	'R1RT1-SBC0NB': 52,
	'H1HTH-SH00N0': 52,
	'H1HT1-SHC0NB': 52,
	'R1RT1-SH00NB': 52,
	'P1PT1-aSRC0NB': 52,
	'H1HTT-TH1RB': 53,
	'H1HTH-TH1RB': 53,
	'P1PT1-TH1RB': 53,
	'R1RT7-TH1RB': 53,
	'R1RT1-TH1R0': 53,
	'H1HT1-TH1R0': 53,
	'P12T1-TH1RB': 53,
	'R1RT1-TH1RB': 53,
	'H1PTH-TH1RB': 53,
	'H1HT1-TH1RH': 53,
	'R1RT1-TH1R8': 53,
	'P1PTH-TH1RB': 53,
	'1171117T1-TH1RB': 53,
	'R1RT1-R0URTH': 54,
	'P1PTH-P0URTH': 54,
	'P1HT7-P0URTH': 54,
	'P1HT1-H0URTH': 54,
	'P1PT1-P0URTH': 54,
	'R1HT1-H0URTH': 54,
	'R1RT1-P0URTH': 54,
	'P1RTH-R0URTH': 54,
	'171HTH-170URTH': 54,
	'P1PT1-P1PTH': 55,
	'P1PT1-P1HTH': 55,
	'R1RT1-H1RTH': 55,
	'P1PTH-P1PTH': 55,
	'H1HT1-H1 HTH': 55,
	'R1RT1-R1RTH': 55,
	'H1HT7-P1PTH': 55,
	'H1PT1-H1PTH': 55,
	'H1HT1-H1HTH': 55,
	'212T1-P1PTH': 55,
	'P1RTH-R1RTH': 55,
	'R1RT1-P1RTH': 55,
	'H1RTH-H1RTH': 55,
	'R1RT1-S1HTH': 56,
	'P1PTH-S1HTH': 56,
	'H1HTH-S1HTH': 56,
	'H1RTH-S1HTH': 56,
	'P1PT1-S1RTH': 56,
	'P1RT1-S18TH': 56,
	'R1PT1-S1RTH': 56,
	'P1PT1-S11TH': 56,
	'H1HT1-S1HTH': 56,
	'P1PT1-S1HTH': 56,
	'R1RT1-S1RTH': 56,
	'R1PT1-S131/BNTH': 56,
	'R1RT1-SHHRNTH': 57,
	'H1HT1-SHHHNTH': 57,
	'H1HT1-SHHBNTH': 57,
	'H1PT7-SBHHNTH': 57,
	'P1PT1-SBHBNTH': 57,
	'111T1-S378NTH': 57,
	'R1PT7-SB7BNTH': 57,
	'P1PTH-SHHHNTH': 57,
	'H1RTH-SHHBNTH': 57,
	'H1HTH-8HHHNTH': 57,
	'H1PTH-SBHBNTH': 57,
	'P1PTH-SBHBNTH': 57,
	}

##################################

main()
