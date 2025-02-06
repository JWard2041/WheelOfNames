function doGet(e) { 
    try {
        // Check if parameters are passed
        if (!e || !e.parameter || !e.parameter.date) {
            return ContentService.createTextOutput(
                JSON.stringify({ error: "Missing 'date' parameter in the request" })
            );
        }

        const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Form Responses 1"); // Adjust to your sheet name
        const data = sheet.getDataRange().getValues(); 

        const targetDate = e.parameter.date; // Date passed as a query parameter
        
        const filtered = [];

        // Loop through rows starting from the second row (skip header)
        for (let i = 1; i < data.length; i++) {
            const timestamp = data[i][0]; // Assuming the first column is the timestamp
            const name = data[i][1]; // Assuming the second column is the name
            const status = data[i][2]; // Assuming the third column contains 'yes' or 'no'

            // Parse and compare the date
            const rowDate = new Date(timestamp);
            rowDate.setMinutes(rowDate.getMinutes() - rowDate.getTimezoneOffset()); // Adjust for timezone
            const localDate = rowDate.toISOString().split("T")[0];
            
            if (localDate === targetDate && status.toLowerCase() === "yes") {
                filtered.push(name); // Collect the name if the date matches and status is 'yes'
            }
        }

        // Log the filtered names for debugging
        Logger.log("Filtered Names: " + JSON.stringify(filtered));

        // Return filtered names as a JSON response
        return ContentService.createTextOutput(JSON.stringify(filtered));
    } catch (err) {
        Logger.log("Error: " + err.message);
        // Return error details in response
        return ContentService.createTextOutput(
            JSON.stringify({ error: err.message })
        );
    }
}
