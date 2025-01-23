module.exports = {
    devServer: {
        host: '0.0.0.0',
        allowedHosts: 'all', 
        client: {
            webSocketURL: 'auto://0.0.0.0/ws'
        },
    },
    
    chainWebpack: (config) => {
        config.resolve.alias.set('vue', '@vue/compat')
    }
      
}
