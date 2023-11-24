export const csrfMixin = {
    data(){
        return {}
    },
    methods: {
        async getCsrfToken(){
            const url = this.$backendURL + '/login';
            await this.$axios.get(url)
            .then(() => {
                // レスポンスを受け取ったときにcsfrトークンがセットされている
            })
            .catch((error) => {
                // 異常処理
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            })
        },
        getCookie(name) {
            if (!document.cookie) {
                return null;
            }
        
            const xsrfCookies = document.cookie.split(';')
                .map(c => c.trim())
                .filter(c => c.startsWith(name + '='));
        
            if (xsrfCookies.length === 0) {
                return null;
            }
            return decodeURIComponent(xsrfCookies[0].split('=')[1]);
        }
    }
}