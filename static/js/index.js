let dataTables = DataTables.default;

Vue.component('tabel-detail', {
    template: '#tabel-detail-template',
    components: {dataTables},
    data: function () {
        return {
            tableData: [],
            dialogFormVisible: false,
            form: {
                name: '',
                id: '',
                format: '',
                description: '',
                comment: ''
            },
            formType: 'create',
            formTitle: '添加影片'
        }
    },
    mounted: function () {
        this.getCategories();
    },
    methods: {
        getActionsDef: function () {
            let self = this;
            return {
                width: 5,
                def: [{
                    name: '添加影片',
                    handler() {
                        self.formType = 'create';
                        self.formTitle = '添加影片';
                        self.form.name = '';
                        self.form.id = '';
                        self.form.format = '';
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
                type: 'rent',
                handler(row) {
                    self.formType = 'edit';
                    self.form.name = row.name;
                    self.form.id = row.id;
                    self.form.format = row.format;
                    self.form.description = row.description;
                    self.form.comment = row.comment;
                    self.formTitle = '编辑数据';
                    self.dialogFormVisible = true;
                },
                name: '借阅'
            }
            ,  {
                type: 'primary',
                handler(row) {
                    self.formType = 'edit';
                    self.form.name = row.name;
                    self.form.id = row.id;
                    self.form.format = row.format;
                    self.form.description = row.description;
                    self.form.comment = row.comment;
                    self.formTitle = '编辑数据';
                    self.dialogFormVisible = true;
                },
                name: '更新影片'
            }, {
                type: 'danger',
                handler(row) {
                        self.$confirm('确认删除该数据?', '提示', {
                            confirmButtonText: '确定',
                            cancelButtonText: '取消',
                            type: 'warning'
                        }).then(function () {
                            let url = Flask.url_for("delete", {name: row.name, id: row.id});
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
            if (self.form.name === '') {
                self.$message.error('影片名称不能为空！');
                return
            }
            if (self.form.format === '') {
                self.form.format = 'BD-ROM'
            }
            if (self.formType === 'create') {
                let url = Flask.url_for("add");
                axios.post(url, {
                    name: self.form.name,
                    format: self.form.format,
                    description: self.form.description,
                    comment: self.form.comment
                }).then(function (response) {
                    self.getCategories();
                    self.dialogFormVisible = false;
                    self.$message.success('添加成功！')
                }).catch(self.showError);
            } else {
                let url = Flask.url_for("update", {});
                axios.put(url, {
                    name: self.form.name,
                    id: self.form.id,
                    format: self.form.format,
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

new Vue({
    el: '#vue-app'
});