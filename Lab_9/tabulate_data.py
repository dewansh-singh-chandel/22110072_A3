from tabulate import tabulate

# Data for the table
data = [
    ["ApplicationProperties",    981.0, 972.0, 140.0, 140.0, 1.015481, 0.844444],
    ["CustomPDFDocumentFactory", 851.0, 841.0,  38.0,   3.0, 0.975610, 0.047619],
    ["UserService",              660.0, 374.0,  15.0,   1.0, 0.853821, 0.000000],
    ["GeneralWebController",     450.0, 435.0,  21.0,  20.0, 0.947619, 0.645161],
    ["YamlHelper",               366.0, 354.0,  21.0,   3.0, 0.950617, 0.107143],
    ["CompressController",       309.0, 293.0,  17.0,   1.0, 0.935385, 0.000000],
    ["GeneralUtils",             300.0,   0.0,  25.0,  18.0, 0.000000, 0.720000],
    ["GeneralUtilsTest",         276.0,   0.0,  24.0,  24.0, 0.000000, 1.000000],
    ["User",                     233.0, 213.0,  11.0,  10.0, 0.954545, 0.391304],
    ["OtherWebController",       230.0, 229.0,  21.0,  20.0, 0.952381, 0.909091],
]

# Column headers
headers = ["Class Name", "LCOM1", "LCOM2", "LCOM3", "LCOM4", "LCOM5", "YALCOM"]

# Print the table with pipe borders
print(tabulate(data, headers=headers, tablefmt="github"))
