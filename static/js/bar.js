Vue.component('foo-detail', {
    template: '#foo-template',
    components: {dataTables},
    data: function () {
        return {
            tableData: [],
            dialogFormVisible: false,
            form: {
                id: '',
                video_name: '',
                video_id: '',
                video_description: '',
                customer_name: '',
                customer_id: '',
                customer_phone: '',
                status: '',
                rental_time: '',
                return_time: '',
                comment: ''
            },
            formType: 'create',
            formTitle: '借阅'
        }
    },
    mounted: function () {
        this.getCategories();
    },
    methods: {






    }
});

new Vue({
    el: '#foo-app'
});