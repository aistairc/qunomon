export const inventoryMixin = {
    data(){
        return {
            result: null,
            name: null,
            filePath: null,
            formats: [],
            selectedFormat: '',
            dataTypes: [],
            selectedType: null,
            description: '',
            errorMessages : [],
            maxCharacters : 100,
            descriptionMaxCharacters : 2000,
            requestData: {
            }
        }
    },
    methods: {
        setInventory(){
            this.requestData.Name = this.name;
            this.requestData.FilePath = this.filePath;
            this.requestData.TypeId = this.selectedType;
            this.requestData.Formats = [this.selectedFormat];
            this.requestData.Description = this.description;
        },
        getFormats(){
            const url = this.$backendURL + '/formats'
            this.$axios.get(url).then((response) => {
                for (var f in response.data.Formats) {
                    this.formats.push(response.data.Formats[f].Format);
                }
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            })
        },
        getDataTypes(){
            const url = this.$backendURL + '/dataTypes'
            this.$axios.get(url).then((response) => {
                this.dataTypes = response.data.DataTypes
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            })
        },
        commonCheckInventory(){
            if(this.name == null || this.name === ""){
                this.errorMessages.push('Name is required.');
            }
            else if(this.name.length > this.maxCharacters){
                this.errorMessages.push('Name must be ' + this.maxCharacters + ' characters or less.');
            }
            if(this.filePath == null || this.filePath === ""){
                this.errorMessages.push('FilePath is required.');
            }
            if(this.selectedType == null || this.selectedType === ""){
                this.errorMessages.push('Type is required.');
            }
            if(this.selectedFormat == null || this.selectedFormat === ""){
                this.errorMessages.push('Format is required.');
            }
            if(this.description.length > this.descriptionMaxCharacters){
                this.errorMessages.push('Description must be ' + this.descriptionMaxCharacters + ' characters or less.');
            }
        },
        checkAndWarnInventoryError(responseData){
            const invenoryErrorCode = ["I20000", "I20001", "I24000", "I24001", "I34000", "I34001", "I34002"];
            if (invenoryErrorCode.includes(responseData.Code)){
                alert(JSON.stringify(responseData, undefined, 4));
                return true;
            } else {
                return false;
            }
        }
    }
}