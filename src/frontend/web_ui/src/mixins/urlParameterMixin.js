export const urlParameterMixin = {
    data() {
        return {
            organizationId: null,
            mlComponentId: null,
            mlComponent: null,
            testDescriptionId: null
        }
    },
    methods: {
        organizationIdCheck(){
            if (!sessionStorage.hasOwnProperty('organizationId')) {
                this.$router.push({
                    name: 'SignIn'
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
                        name: 'SignIn'
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
                    params: {error}
                }).catch(error => {
                    // eslint-disable-next-line no-console
                    console.log(error)
                })
            });
        }
    }
}