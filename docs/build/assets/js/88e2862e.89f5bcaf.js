"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[9703],{32450:(e,t,r)=>{r.r(t),r.d(t,{assets:()=>b,contentTitle:()=>G,default:()=>D,frontMatter:()=>m,metadata:()=>s,toc:()=>y});const s=JSON.parse('{"id":"chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete","title":"Delete User Group","description":"Delete User Group","source":"@site/docs/chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete","permalink":"/docs/chatbot-api/delete-user-group-manage-admin-user-group-user-group-id-delete","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"delete-user-group-manage-admin-user-group-user-group-id-delete","title":"Delete User Group","description":"Delete User Group","sidebar_label":"Delete User Group","hide_title":true,"hide_table_of_contents":true,"api":"eJyVVE1v2zAM/SsGTxug1Vm3k2/dGmxFO6zoxy5BELA2k6ixLVWSiwWG/vtAyY5tuD3sksgSST2+96gWlCaDTqr6qoAMCirJ0aaxZDY7oxq9qbDGHW2wqGQ93h+vZbHZxEwQoNFgRY6MhWzVgqGXRhoqIHOmIQE231OFkLXgjpogA1k72pEBAU66knceLZnkB1dOrgrwAmqseH9yIwiQNWSg0e3BrwUYslrVlizXPl8s+K8gmxupuT3I4L7Jc7J225TJXRcMAnJVO6odh6PWpcwDG+mz5Zx2wOu99wK+np/PC//BUhYhLVkao8x/VAVtWAEnI+6CHMqSV9JRZecBpconp1gff28D0R2d1hlZ78CLGcF+7UW/h8bgcUT5jYoAme3K7kbydPWG0F9kLe4ITsXeDw1kJA986oe71dMz5Q7EyBqr0Fe8uotbD2UGeiO777dxGel767I+5OfDw+2sYNTWUt4Y6Y6Bzovbq2s6flfqIAmy1ZotNlX9Mjg+GdzKDZDbq2GQwji4PWSQxjlKwxyl7ORPwclpO3G1B4ZhXvvpaUwJGeyd01malirHcq+sy74sFotg+h7yPfspOmQK/CQOanlNx35q8nh8Gq0tWodaMhaLDU+U58itChU66u6x0iUl3zA/UM0DyDAjF4uzxdlnFkYr6yoMHu9Kv0XThMgTREd/XapLlMGGofW2428FkT8QEBgEAQOHICCbvg1rAcwT57XtE1p6NKX3vP3SkGGB1wJe0Uh84s5WLRTS8rqAbIulpRnE0zzDh7vOth8TEG9D7ymvme9XLBv+AgEHOs6esTCVe8KCTAASYy7ynLQbZc8eEVb/5LbL5c3yYcnksHYT0Q9B9G4xeiem4Gb692D5d/SWTLPaNrrK+1N8PHo3o2u0j2a61t77f5YdPSE=","sidebar_class_name":"delete api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Create User Group","permalink":"/docs/chatbot-api/create-user-group-manage-admin-user-group-post"},"next":{"title":"Patch User Group","permalink":"/docs/chatbot-api/patch-user-group-manage-admin-user-group-user-group-id-patch"}}');var o=r(74848),a=r(28453),i=r(57742),p=r.n(i),n=r(78178),d=r.n(n),l=r(19624),u=r.n(l),c=r(96226),g=r.n(c),h=(r(77675),r(19365),r(51107));const m={id:"delete-user-group-manage-admin-user-group-user-group-id-delete",title:"Delete User Group",description:"Delete User Group",sidebar_label:"Delete User Group",hide_title:!0,hide_table_of_contents:!0,api:"eJyVVE1v2zAM/SsGTxug1Vm3k2/dGmxFO6zoxy5BELA2k6ixLVWSiwWG/vtAyY5tuD3sksgSST2+96gWlCaDTqr6qoAMCirJ0aaxZDY7oxq9qbDGHW2wqGQ93h+vZbHZxEwQoNFgRY6MhWzVgqGXRhoqIHOmIQE231OFkLXgjpogA1k72pEBAU66knceLZnkB1dOrgrwAmqseH9yIwiQNWSg0e3BrwUYslrVlizXPl8s+K8gmxupuT3I4L7Jc7J225TJXRcMAnJVO6odh6PWpcwDG+mz5Zx2wOu99wK+np/PC//BUhYhLVkao8x/VAVtWAEnI+6CHMqSV9JRZecBpconp1gff28D0R2d1hlZ78CLGcF+7UW/h8bgcUT5jYoAme3K7kbydPWG0F9kLe4ITsXeDw1kJA986oe71dMz5Q7EyBqr0Fe8uotbD2UGeiO777dxGel767I+5OfDw+2sYNTWUt4Y6Y6Bzovbq2s6flfqIAmy1ZotNlX9Mjg+GdzKDZDbq2GQwji4PWSQxjlKwxyl7ORPwclpO3G1B4ZhXvvpaUwJGeyd01malirHcq+sy74sFotg+h7yPfspOmQK/CQOanlNx35q8nh8Gq0tWodaMhaLDU+U58itChU66u6x0iUl3zA/UM0DyDAjF4uzxdlnFkYr6yoMHu9Kv0XThMgTREd/XapLlMGGofW2428FkT8QEBgEAQOHICCbvg1rAcwT57XtE1p6NKX3vP3SkGGB1wJe0Uh84s5WLRTS8rqAbIulpRnE0zzDh7vOth8TEG9D7ymvme9XLBv+AgEHOs6esTCVe8KCTAASYy7ynLQbZc8eEVb/5LbL5c3yYcnksHYT0Q9B9G4xeiem4Gb692D5d/SWTLPaNrrK+1N8PHo3o2u0j2a61t77f5YdPSE=",sidebar_class_name:"delete api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},G=void 0,b={},y=[];function x(e){const t={p:"p",...(0,a.R)(),...e.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(h.default,{as:"h1",className:"openapi__heading",children:"Delete User Group"}),"\n",(0,o.jsx)(p(),{method:"delete",path:"/manage/admin/user-group/{user_group_id}",context:"endpoint"}),"\n",(0,o.jsx)(t.p,{children:"Delete User Group"}),"\n",(0,o.jsx)(h.default,{id:"request",as:"h2",className:"openapi-tabs__heading",children:"Request"}),"\n",(0,o.jsx)(d(),{parameters:[{required:!0,schema:{type:"integer",title:"User Group Id"},name:"user_group_id",in:"path"}]}),"\n",(0,o.jsx)(u(),{title:"Body",body:void 0}),"\n",(0,o.jsx)(g(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{}}}},422:{description:"Validation Error",content:{"application/json":{schema:{properties:{detail:{items:{properties:{loc:{items:{anyOf:[{type:"string"},{type:"integer"}]},type:"array",title:"Location"},msg:{type:"string",title:"Message"},type:{type:"string",title:"Error Type"}},type:"object",required:["loc","msg","type"],title:"ValidationError"},type:"array",title:"Detail"}},type:"object",title:"HTTPValidationError"}}}}}})]})}function D(e={}){const{wrapper:t}={...(0,a.R)(),...e.components};return t?(0,o.jsx)(t,{...e,children:(0,o.jsx)(x,{...e})}):x(e)}}}]);