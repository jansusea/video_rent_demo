let dataTables = DataTables.default;

const Raw = Vue.component('rental-detail', {
    template: '#raw-template',
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
            formTitle: '借阅',

            options: [{
              status: '1',
              label: '租赁中'
                }, {
              status: '0',
              label: '已归还'
                }],
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
                    self.form.status = row.status;
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
                            let url = Flask.url_for("delete_rental", {name: row.video_name, id: row.id});
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
                    rental_time: moment(self.form.rental_time).format("YYYY-MM-DD HH:mm:ss"),
                    return_time: moment(self.form.return_time).format("YYYY-MM-DD HH:mm:ss"),
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
                    rental_time: moment(self.form.rental_time).format("YYYY-MM-DD HH:mm:ss"),
                    return_time: moment(self.form.return_time).format("YYYY-MM-DD HH:mm:ss"),
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
        },
        formatStatus: function(status) {//将后台传过来的valueOf格式的时间改成yyyy/m/d的格式
　　      if(status === "1"){
                return "租赁中"
            }else {
                return "已归还"
            }
},
    }
});

const customer = Vue.component('customer-detail', {
    template: '#customer-template',
    components: {dataTables},
    data: function () {
        return {
            tableData: [],
            dialogFormVisible: false,
            form: {
                id: '',
                name: '',
                phone: '',
                deposit: '',
                comment: ''
            },
            formType: 'create',
            formTitle: '添加会员'
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
                    name: '添加会员',
                    handler() {
                        self.formType = 'create';
                        self.formTitle = '添加会员';
                        self.form.id = '';
                        self.form.phone = '';
                        self.form.name = '';
                        self.form.deposit = '';
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
                    self.form.name = row.name;
                    self.form.phone = row.phone;
                    self.form.deposit = row.deposit;
                    self.form.comment = row.comment;
                    self.formTitle = '编辑数据';
                    self.dialogFormVisible = true;
                },
                name: '编辑'
            }, {
                type: 'danger',
                handler(row) {
                        self.$confirm('确认删除该会员数据?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(function () {
                            let url = Flask.url_for("delete_customer", {id: row.id});
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
            let url = Flask.url_for("get_customer_data");
            let self = this;
            axios.get(url).then(function (response) {
                self.tableData = response.data.results;
            });
        },
        createOrUpdate: function () {
            let self = this;
            if (self.formType === 'create') {
                let url = Flask.url_for("add_customer");
                axios.post(url, {
                    phone: self.form.phone,
                    name: self.form.name,
                    deposit: self.form.deposit,
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
                     phone: self.form.phone,
                    name: self.form.name,
                    deposit: self.form.deposit,
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

const video = Vue.component('video-detail', {
    template: '#video-template',
    components: {dataTables},
    data: function () {
        return {
            tableData: [],
            dialogFormVisible: false,
            form: {
                id: '',
                name: '',
                description: '',
                comment: ''
            },
            formType: 'create',
            formTitle: '增加影片'
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
                    name: '增加影片',
                    handler() {
                        self.formType = 'create';
                        self.formTitle = '增加影片';
                        self.form.id = '';
                        self.form.name = '';
                        self.form.description = '';
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
                    self.form.name = row.name;
                    self.form.description = row.description;
                    self.form.comment = row.comment;
                    self.formTitle = '编辑数据';
                    self.dialogFormVisible = true;
                },
                name: '编辑'
            }, {
                type: 'danger',
                handler(row) {
                        self.$confirm('确认删除该影片数据?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(function () {
                            let url = Flask.url_for("delete_video", {id: row.id});
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
            let url = Flask.url_for("get_video_data");
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
                let url = Flask.url_for("add_video");
                axios.post(url, {
                    name: self.form.name,
                    description: self.form.description,
                    comment: self.form.comment
                }).then(function (response) {
                    self.getCategories();
                    self.dialogFormVisible = false;
                    self.$message.success('添加成功！')
                }).catch(self.showError);
            } else {
                let url = Flask.url_for("update_video", {});
                axios.put(url, {
                    id: self.form.id,
                    name: self.form.name,
                    description: self.form.description,
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

const routes = [
  { path: '/', component: Raw },
  { path: '/customer', component: customer },
  { path: '/video', component: video}
]

const router = new VueRouter({
  routes // (缩写) 相当于 routes: routes
})


const app = new Vue({
  router
}).$mount('#foo_app')