export const MLComponentMixin = {
    data(){
        return {
            result: null,
            name: null,
            description: null,
            problem_domain: null,
            mlFrameworks: null,
            select_guideline_id: -1,
            guidelines: null,
            select_scope_id: -1,
            scopes: [],
            all_scopes: null,
            guideline_reason: null,
            scope_reason: null,
            errorMessages : [],
            maxCharacters : 256,
            descriptionMaxCharacters : 2048,
            requestData: {
            }
        }
    },
    methods: {
        getGuidelines(){
            const url = this.$backendURL + '/guidelines'
            this.$axios.get(url).then((response) => {
                this.guidelines = response.data.Guidelines
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            })
        },
        getScopes(){
            const url = this.$backendURL + '/scopes'
            this.$axios.get(url).then((response) => {
                this.all_scopes = response.data.Scopes
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            })
        },
        setScopeList(){
            this.scopes = [];
            for (let row in this.all_scopes){
                // 選択したガイドラインIDを持つscopeだけリスト表示
                if (this.all_scopes[row].GuidelineId == this.select_guideline_id){
                    this.scopes.push(this.all_scopes[row])
                }
            }
        },
        setMLComponent(){
            this.requestData.Name = this.name;
            this.requestData.Description = this.description;
            this.requestData.ProblemDomain = this.problem_domain;
            this.requestData.MLFrameworkId = 0;
            this.requestData.GuidelineId = this.select_guideline_id;
            this.requestData.ScopeId = this.select_scope_id;
            this.requestData.GuidelineReason = this.guideline_reason;
            this.requestData.ScopeReason = this.scope_reason;
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
            if(this.select_guideline_id == -1){
                this.errorMessages.push('Guideline is required.');
            }
            if(this.select_scope_id == -1){
                this.errorMessages.push('Scope is required.');
            }
        }
    }
}