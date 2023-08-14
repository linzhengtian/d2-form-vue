xadmin基类和方法如下所示，可以通过重写以下方法，扩展xadmin相关功能：

```
一、BaseAdminObject 类
1.1 get_admin_url() 方法
1.2 get_form_params() 方法
1.3 get_model_perm() 方法
1.4 get_model_url() 方法
1.5 get_model_view() 方法
1.6 get_query_string() 方法
1.7 get_view() 方法
1.8 has_model_perm() 方法
1.9 message_user() 方法
1.10 render_response() 方法
1.11 static() 方法
1.12 template_response() 方法
二、BaseAdminPlugin 类
2.1 filter_hook() 方法
2.2 init_request() 方法
三、BaseAdminView 类
3.1 as_view() 类方法
3.2 get_context() 方法
3.3 get_media() 方法
3.4 init_plugin() 方法
3.5 init_request() 方法
四、CommAdminView 类
4.1 get_breadcrumb() 方法
4.2 get_context() 方法
4.3 get_model_icon() 方法
4.4 get_nav_menu() 方法
4.5 get_site_menu() 方法
五、ModelAdminView 类
5.5 get_breadcrumb() 方法
5.2 get_context() 方法
5.3 get_model_perms() 方法
5.4 get_object() 方法
5.5 get_object_url() 方法
5.6 get_ordering() 方法
5.7 get_template_list() 方法
5.8 has_add_permission() 方法
5.9 has_change_permission() 方法
5.10 has_delete_permission() 方法
5.11 has_view_permission() 方法
5.12 model_admin_url() 方法
5.13 queryset() 方法
六、ListAdminView 类
6.1 get() 方法
6.2 get_check_field_url() 方法
6.3 get_context() 方法
6.4 get_list_display() 方法
6.5 get_list_display_links() 方法
6.6 get_list_queryset() 方法
6.7 get_media() 方法
6.8 get_model_method_fields() 方法
6.9 get_ordering() 方法
6.10 get_ordering_field() 方法
6.11 get_ordering_field_columns() 方法
6.12 get_page_number() 方法
6.13 get_paginator() 方法
6.14 get_response() 方法
6.15 get_result_list() 方法
6.16 init_request() 方法
6.17 make_result_list() 方法
6.18 post() 方法
6.19 post_response() 方法
6.20 post_result_list() 方法
6.21 result_header() 方法
6.22 result_headers() 方法
6.23 result_item() 方法
6.24 result_row() 方法
6.25 results() 方法
6.26 url_for_result() 方法
七、ModelFormAdminView 类
7.1 formfield_for_dbfield() 方法
7.2 get() 方法
7.3 get_context() 方法
7.4 get_error_list() 方法
7.5 get_field_attrs() 方法
7.6 get_field_style() 方法
7.7 get_form_helper() 方法
7.8 get_form_layout() 方法
7.9 get_media() 方法
7.10 get_model_form() 方法
7.11 get_readonly_fields() 方法
7.12 instance_forms() 方法
7.13 post() 方法
7.14 prepare_form() 方法
7.15 save_forms() 方法
7.16 save_models() 方法
7.17 save_related() 方法
7.18 setup_forms() 方法
7.19 valid_forms() 方法
八、CreateAdminView 类
8.1 get_breadcrumb() 方法
8.2 get_context() 方法
8.3 get_form_datas() 方法
8.4 get_response() 方法
8.5 post_response() 方法
九、UpdateAdminView 类
9.1 get_breadcrumb() 方法
9.2 get_context() 方法
9.3 get_form_datas() 方法
9.4 get_response() 方法
9.5 post_response() 方法
十、DeleteAdminView 类
10.1 delete_model() 方法
10.2 get() 方法
10.3 get_breadcrumb() 方法
10.4 get_context() 方法
10.5 init_request() 方法
10.6 post() 方法
10.7 post_response() 方法
十一、DetailAdminView 类
11.1 get() 方法
11.2 get_breadcrumb() 方法
11.3 get_context() 方法
11.4 get_field_result() 方法
11.5 get_form_helper() 方法
11.6 get_form_layout() 方法
11.7 get_media() 方法
11.8 get_model_form() 方法
11.9 get_response() 方法
11.10 init_request() 方法
十二、filter_hook() 方法
十三、csrf_protect_m() 方法
```