export const MLComponentMixin = {
    data(){
        return {
            result: null,
            name: null,
            description: null,
            problem_domain: null,
            select_ml_framework_id: -1,
            mlFrameworks: null,
            errorMessages : [],
            maxCharacters : 256,
            descriptionMaxCharacters : 2048,
            requestData: {
            }
        }
    },
    methods: {
        getMLFrameworks(){
            const url = this.$backendURL + '/mlFrameworks'
            this.$axios.get(url).then((response) => {
                this.mlFrameworks = response.data.MLFrameworks
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            })
        },
        setMLComponent(){
            this.requestData.Name = this.name;
            this.requestData.Description = this.description;
            this.requestData.ProblemDomain = this.problem_domain;
            this.requestData.MLFrameworkId = this.select_ml_framework_id;
        },
        commonCheckMLComponent(){
            if(this.name == null || this.name === ""){
                this.errorMessages.push('Name is required.');
            }
            else if(this.name.length > this.maxCharacters){
                this.errorMessages.push('Name must be ' + this.maxCharacters + ' characters or less.');
            }
            if(this.description == null || this.description === ""){
                this.errorMessages.push('Description is required.');
            }
            else if(this.description.length > this.descriptionMaxCharacters){
                this.errorMessages.push('Description must be ' + this.descriptionMaxCharacters + ' characters or less.');
            }
            if(this.problem_domain == null || this.problem_domain === ""){
                this.errorMessages.push('ProblemDomain is required.');
            }
            else if(this.problem_domain.length > this.maxCharacters){
                this.errorMessages.push('ProblemDomain must be ' + this.maxCharacters + ' characters or less.');
            }
            if(this.select_ml_framework_id == -1){
                this.errorMessages.push('MLFrameworkName is required.');
            }
        },
        signOut() {
            sessionStorage.clear();
            this.$router.push({
                name: 'SignIn'
            });
        }
    }
}