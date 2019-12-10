let dataTables = DataTables.default;

Vue.component('tabel-detail', {
    template: '#tabel-detail-template',
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
        getActionsDef: function () {
            let self = this;
            return {
                width: 9,
                def: [{
                    name: '借阅',
                    handler() {
                        self.formType = 'create';
                        self.formTitle = '借阅';
                        self.form.id = '';
                        self.form.video_name = '';
                        self.form.video_description = '';
                        self.form.customer_phone = '';
                        self.form.customer_name = '';
                        self.form.rental_time = '';
                        self.form.return_time = '';
                        self.form.comment = '';
                        self.dialogFormVisible = true;
                    },
                    icon: 'plus'
                }]
            }
        },
        getPaginationDef: function () {
            return {
                pageSize: 10,
                pageSizes: [10, 20, 50]
            }
        },
        getRowActionsDef: function () {
            let self = this;
            return [
                {
                type: 'primary',
                handler(row) {
                    self.formType = 'edit';
                    self.form.id = row.id;
                    self.form.video_name = row.video_name;
                    self.form.video_description = row.video_description;
                    self.form.rental_time = row.rental_time;
                    self.form.return_time = row.return_time;
                    self.form.customer_name = row.customer_name;
                    self.form.customer_phone = row.customer_phone;
                    self.form.comment = row.comment;
                    self.formTitle = '编辑数据';
                    self.dialogFormVisible = true;
                },
                name: '编辑'
            }, {
                type: 'danger',
                handler(row) {
                        self.$confirm('确认删除该数据?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(function () {
                            let url = Flask.url_for("delete", {name: row.video_name, id: row.id});
                            console.log(url)
                            axios.delete(url).then(function (response) {
                                self.getCategories();
                                self.$message.success("删除成功！")
                            }).catch(self.showError)
                        });

                    // }
                },
                name: '删除'
            }]
        },
        getCategories: function () {
            let url = Flask.url_for("get_base_data");
            let self = this;
            axios.get(url).then(function (response) {
                self.tableData = response.data.results;
            });
        },
        createOrUpdate: function () {
            let self = this;
            if (self.form.video_name === '') {
                self.$message.error('影片名称不能为空！');
                return
            }
            if (self.formType === 'create') {
                let url = Flask.url_for("add_rental");
                axios.post(url, {
                    video_name: self.form.video_name,
                    video_description: self.form.video_description,
                    customer_phone: self.form.customer_phone,
                    customer_name: self.form.customer_name,
                    rental_time: self.form.rental_time,
                    return_time: self.form.return_time,
                    comment: self.form.comment
                }).then(function (response) {
                    self.getCategories();
                    self.dialogFormVisible = false;
                    self.$message.success('添加成功！')
                }).catch(self.showError);
            } else {
                let url = Flask.url_for("update_rental", {});
                axios.put(url, {
                    id: self.form.id,
                    video_name: self.form.video_name,
                    video_description: self.form.video_description,
                    customer_phone: self.form.customer_phone,
                    customer_name: self.form.customer_name,
                    rental_time: self.form.rental_time,
                    return_time: self.form.return_time,
                    status: self.form.status,
                    comment: self.form.comment
                }).then(function (response) {
                    self.getCategories();
                    self.dialogFormVisible = false;
                    self.$message.success('修改成功！')
                }).catch(self.showError);
            }
        },
        showError: function (error) {
            let response = error.response;
            this.$message.error(response.data.message);
        }
    }
});

new Vue({
    el: '#vue-app'
});