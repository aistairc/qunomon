// URLサニタイズ
var sanitizeUrl = require("@braintree/sanitize-url").sanitizeUrl;

export const urlParameterMixin = {
    data() {
        return {
            organizationId: null,
            mlComponentId: null,
            mlComponent: null,
            testDescriptionId: null,
            organizationIdNotFoundError: {
                response:{
                    data:{
                        Code: '',
                        message: 'OrganizationId not found.'
                    }
                }
            }
        }
    },
    methods: {
        organizationIdCheck_method(){
            if (!sessionStorage.hasOwnProperty('organizationId')) {
                this.$router.push({
                    name: 'Information',
                    query: {error: JSON.stringify(this.organizationIdNotFoundError)}
                })
            }
        },
        mlComponentIdCheck(){
            if (!sessionStorage.hasOwnProperty('mlComponentId')) {
                if (sessionStorage.hasOwnProperty('organizationId')) {
                    this.$router.push({
                        name: 'MLComponents'
                    })
                }
                else{
                    this.$router.push({
                        name: 'Information',
                        query: {error: JSON.stringify(this.organizationIdNotFoundError)}
                    })
                }
            }
        },
        getMLComponent(){
            const url = this.$backendURL
                        + '/'
                        + this.organizationIdCheck
                        + '/mlComponents';
            this.$axios.get(url)
            .then((response) => {
                const mlComponents = response.data.MLComponents
                this.mlComponent = mlComponents.find((m) => m.Id == this.mlComponentId);
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                }).catch(error => {
                    // eslint-disable-next-line no-console
                    console.log(error)
                })
            });
        },
        cleanUrl(val) {
            // URLをサニタイズする
            return sanitizeUrl(val);
        }
    }
}