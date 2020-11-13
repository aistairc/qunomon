export const inventoryMixin = {
    data(){
        return {
            result: null,
            name: null,
            filePath: null,
            selectedType: '',
            selectedFileSystem: '',
            formats: null,
            formatList: [],
            formatTypes: [],
            selectedFormats: [],
            dataTypes: [],
            fileSystems: [],
            description: '',
            errorMessages : [],
            maxCharacters : 100,
            descriptionMaxCharacters : 2000,
            requestData: {
            },
            selectedFormatType: ''
        }
    },
    created() {
        this.getFormats();
    },
    methods: {
        setInventory(){
            this.requestData.Name = this.name;
            this.requestData.FilePath = this.filePath;
            //DataType入る
            this.requestData.DataTypeId = this.selectDataType;
            
            this.requestData.FileSystemId = this.selectedFileSystem;
            this.requestData.TypeId = this.selectedType;
            this.requestData.Formats = this.selectedFormats;
            this.requestData.Description = this.description;
        },
        getFormats(){
            const url = this.$backendURL + '/formats'
            this.$axios.get(url).then((response) => {
                this.formats = response.data.Formats
                this.formatList = this.formats;
                this.setFormatTypes();
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
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
                    params: {error}
                })
            })
        },
        getFileSystems(){
            const url = this.$backendURL + '/fileSystems'
            this.$axios.get(url).then((response) => {
                this.fileSystems = response.data.FileSystems
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            })
        },
        setFormatTypes(){
            var tempFormatTypes = [];
            for(var format of this.formats){
                tempFormatTypes.push(format.Type);
            }
            this.formatTypes = tempFormatTypes.filter((x, i, self) => self.indexOf(x) === i);
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
            else if(this.selectedFileSystem === 1){
                if(encodeURIComponent(this.filePath).replace(/%../g,"x").length > 1023){
                    this.errorMessages.push('FilePath must be 1023 bytes or less.');
                }
                for(var filePathItem of this.filePath.split('/')){
                    if(encodeURIComponent(filePathItem).replace(/%../g,"x").length > 255){
                        this.errorMessages.push('All directory and file names must be 255 bytes or less.');
                        break;
                    }
                }
            }
            else if(this.selectedFileSystem === 2){
                if(this.filePath.length > 259){
                    this.errorMessages.push('FilePath must be 259 characters or less.');
                }
            }
            if(this.selectedType == null || this.selectedType === ""){
                this.errorMessages.push('Type is required.');
            }
            if(this.selectedFileSystem == null || this.selectedFileSystem === ""){
                this.errorMessages.push('FileSystem is required.');
            }
            if(this.description.length > this.descriptionMaxCharacters){
                this.errorMessages.push('Description must be ' + this.descriptionMaxCharacters + ' characters or less.');
            }
            if(this.selectedFormats.length === 0){
                this.errorMessages.push('Format is required.');
            }
        },
        getFileName(filePath) {
            var posix_file_pos = filePath.lastIndexOf('/');
            var win_file_pos = filePath.lastIndexOf('\\');
            var file_name = ''
            if (posix_file_pos != -1){
                file_name = filePath.slice(posix_file_pos + 1);
            }else {
                file_name = filePath.slice(win_file_pos + 1);
            }
            return file_name;
        },
        changeFormatList() {
            this.formats = this.formatList;
            var tmp_formatList = [];
            var cnt = 0;
            for (var format in this.formats) {
                if (this.formats[format].Type == this.selectedFormatType) {
                    tmp_formatList[cnt] = this.formats[format];
                    ++cnt;
                }
            }
            this.formats = tmp_formatList;
            this.selectedFormats = "";
        },
        changeFormatTypeList() {
            var tmp_selectedFormats = this.selectedFormats;
            if (this.selectedFormatType == null || this.selectedFormatType == '') {
                for (var format in this.formatList) {
                    if (this.selectedFormats == this.formatList[format].Format) {
                        this.selectedFormatType = this.formatList[format].Type;
                        this.changeFormatList();
                        this.selectedFormats = tmp_selectedFormats;
                        break;
                    }
                }
            }
        },
        checkFormat() {
            this.isInvalidFormat = false;
            if (this.filePath == null){
                return;
            }

            var file_name = this.getFileName(this.filePath)
            var pos = file_name.lastIndexOf('.');
            if (pos != -1) {
                var ext = file_name.slice(pos + 1)
                for (var format in this.formatList) {
                    if (this.formatList[format].Format == ext) {
                        this.selectedFormatType = this.formatList[format].Type;
                        this.changeFormatList();
                        this.selectedFormats = this.formatList[format].Format;
                        return;
                    }
                }
                // 全てのフォーマットをチェックして、無かった場合
                this.isInvalidFormat = true;
            }
            else{
                this.selectedFormatType = 'binary';
                this.changeFormatList();
                this.selectedFormats = '*';
            }
        },
    }
}