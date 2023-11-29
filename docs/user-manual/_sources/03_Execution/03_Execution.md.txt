# Execution

## Register report template (optional)

Original report templates can be registered.

(This is not a required task, as the report can be output without a template.)

### Create report template

#### When create your own report template

A sample template exists in the folder below, please copy, edit and zip it.

qunomon\src\backend\report\templates\1

#### When create a report template from guideline

In the "Create Report Template" portion of the ReportTemplate screen, select a guideline and click the "Create" button.

![0101](01/01.png)

### Register report template

In the "Install Report Template" portion of the ReportTemplate screen, select the guideline to be associated with.

Next, enter a template name, upload the zipped template file, and click the "install" button.

![0102](01/02.png)

## Register MLComponents

MLComponent is a unit that represents one machine learning model.

When you press the "Create" button on the MLComponents screen, the MLComponent new creation screen will be displayed.

![0201](02/01.png)

Enter the necessary items in the MLComponent new creation screen and click the "Create" button.

MLComponentName：Enter MLComponent Name

Description：Enter MLComponent Description

Domain：Enter MLComponent Domain

Guideline：Select the guideline to be used

Scope：Select the scope to be used in the guideline

![0202](02/02.png)

The created MLComponent will appear in the list on the MLComponents screen, so press the "test" icon.

![0203](02/03.png)

![0204](02/04.png)

## Register Inventories

Inventory is a function that manages information on machine learning models and CSV-like data used in AIT.

Basically, registration is done from the Inventory registration screen, but it can also be done from the TestDescriptions registration screen.

Click "Inventories" from the submenu to display the Inventory list screen, then press the "Create" button.

![0301](03/01.png)

Enter the required fields on the Create New Inventory screen and click the "Create" button.

Name：Enter Inventory name

Path：Enter file path where the Inventory is saved

DataType：Select "dataset", "model" or "attribute set" (Must be the same type of Inventory used by AIT)

Format：Select a file extension (or type directly if not available)

Description：Inventory description

![0302](03/02.png)

## Register TestDescriptions

TestDescription is the unit of test to be performed on Qunomon.

Click the "Create" button on the TestDescription screen to move to the creation screen.

![0401](04/01.png)

Enter basic information for TestDescription and click the "Next" button.

General→Name：Enter TestDescription name

AIT Program：Select the AIT to be used (you can filter by "Name" or "Description")

Quality Dimension：Select the quality that AIT measures

![0402](04/02.png)

Enter detailed information for TestDescription and click the "Create" button.

Acceptance Criteria：Enter the AIT evaluation value (if all of this formula is satisfied when executing TestDescription, the TestDescription execution result will be OK)

AIT Parameter：Enter AIT parameters

Target Inventories：Select the inventory to be used by AIT (Inventories can also be registered using the "+" icon here)

![0403](04/03.png)

If successfully registered, it will be added to the TestDescription list.

![0404](04/04.png)

## Run TestDescriptions

Select the TestDescription to run and execute it with "Run test".

![0501](05/01.png)

When finished, the Status of the selected TestDescription changes.

OK：If Acceptance Criteria are satisfied

NG：If Acceptance Criteria cannot be satisfied

ERR：If TestDescription could not be executed

![0502](05/02.png)

* How to investigate the cause of ERR

(1) Confirm the details of the error on the detail screen of the TestDescription that resulted in an ERR.

(2) Confirm log files in the "qai-testbed\qunomon\logs" directory

(3) Confirm airflow logs

Access "http://localhost:8180/home" and check the log of AIT used in TestDescription.

(ID：airflow　PASS：airflow)

## TestDescriptions Details Display

Click the detail icon for the target TestDescription.

![0601](06/01.png)

![0602](06/02.png)

Once you select the Test Result output file, you can view its contents.

"Report Contents" allows you to set whether to include the output file in the report.

"Opinion" allows you to add a general review to the report.

![0603](06/03.png)

Click "Download" in the submenu or "Click here to download the data" to go to the Download screen.

![0604](06/04.png)

## Download Resources

Click the download icon to download the file.

![0701](07/01.png)

## Copy TestDescription

By pressing the "Copy" icon of TestDescriptions on the TestDescription list screen, you can copy and create the contents.

![0801](08/01.png)

Edit "Name", "Acceptance Criteria", "AIT Parameter" and "Target Inventories" and click the "Create" button.

![0802](08/02.png)

It will be added to the TestDescription list screen.

![0803](08/03.png)

After executing the copied TestDescription, a "relationsip" icon will appear. 

Click on that icon to view the parent-child relationship of the TestDescription.

![0804](08/04.png)

![0805](08/05.png)

## Compare TestDescriptions

If you select two TestDescriptions that have a parent-child relationship and click the "Compare" button, you can transition to the comparison screen.

![0901](09/01.png)

![0902](09/02.png)

Select an output file to display it on the screen.

![0903](09/03.png)

## Report Output

Select TestDescription and click the "Download Report" button to output the report.

![1001](10/01.png)

On the report template selection screen, select the template you created and click the "Preview" button to preview the report using the template.

Alternatively, select "Do not use ReportTemplate" and click the "Preview" button to preview the report without the template.

![1002](10/02.png)

The string entered in "Report Opinion" will be reflected in the report's overall rating.

Click the "Create" button to download the report in PDF format.

![1003](10/03.png)


