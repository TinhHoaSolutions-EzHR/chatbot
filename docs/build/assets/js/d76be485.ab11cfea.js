"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[2818],{25472:(e,t,o)=>{o.r(t),o.d(t,{assets:()=>f,contentTitle:()=>h,default:()=>g,frontMatter:()=>C,metadata:()=>a,toc:()=>y});const a=JSON.parse('{"id":"chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post","title":"Create Deletion Attempt For Connector Id","description":"Create Deletion Attempt For Connector Id","source":"@site/docs/chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post","permalink":"/docs/chatbot-api/create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post","title":"Create Deletion Attempt For Connector Id","description":"Create Deletion Attempt For Connector Id","sidebar_label":"Create Deletion Attempt For Connector Id","hide_title":true,"hide_table_of_contents":true,"api":"eJyVVU1vGjEQ/SurOW/CNu1pb2mSqiitggLtBa3Q4B3AwWtvbG8ShPa/V2Mv30FpLmDs+XzvzbAGU5NFL43ul5CDsISeJiUp4rsJek9V7SczYyfCaE3CGzuR5aRCjXOaYFlJfWpeG+chBUvPDTn/3ZQryNcgjPakPR+xrpUUIW/vyRnNd04sqEI+1Zar8pJc57bNy7/9qibIQWpPc7KQgpde8c3NxjDpl9Cm3ExJ2ktUH3puLYNrm25MzfSJxKYVaamEfHxY0HGa4p16duEHKG0/nGeSLLScahfa24bChauNdrH7qyzjr5KcsLJmwCCHYSMEOTdrVPLYGXMh/4lvG9J+u7o6DfwXlSyDW3JnrbGfiHrEWkkepeKT9FS5UwNlxMEr6tXDDPLxlibnrdRzaNMT4tpixxBai6s9Kn+ZWCALoHLzPdq7eDvT3+Qczgm2wc6bBjCSEb9+pA7uK6bu7PYUsYM3onu+jdsI33vJNiY/R6PBScDIrSPRWOlXAc7rQf+eVjfGLCVBPi7aIj1i/SZMfXLbjXFyHcc4+WFscjBUKVTkF4Y3RTfiNfoF5NCL+6AX9kFvsw8uun0AXJF9IetCQY1VkMPC+zrv9ZQRqBbG+fxrlmXAxW2qH7K0olgOe9jyhLW8J4ZNchsiPqegseLXGTqPtWwcWYeNXwQ0WbePu71094ZVreh0z2Qn+yNrOc/MhPwdB8PgnXxHsSTN+HCTEdTsMrv8wgwzUhWGYekK+wTeB0Rt+/b05nu1QhlkHvBcd1SMIVIBKQQyQowjOooUGHE2Xq+n6OiPVW3L188NWVZNkcILWolTFSWTwoKwJBv4W9IqbjfeCxdhKNhcNZGSox3B8xs9roWgIIbztsWewgYPwxGkMO3+PSpTso/FVx44fIUcIAUToAkaCXdrUKjnDQOQQ4zJrAf6D3SzDLrpDntbB/Vqr8ITCaVdL/y5t5kOvdbrKMy23drHp7MeHboba+a1aNv2H16Qo34=","sidebar_class_name":"post api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Delete Genai Api Key","permalink":"/docs/chatbot-api/delete-genai-api-key-manage-admin-genai-api-key-delete"},"next":{"title":"Promote Admin","permalink":"/docs/chatbot-api/promote-admin-manage-promote-user-to-admin-patch"}}');var n=o(74848),i=o(28453),r=o(57742),c=o.n(r),d=o(78178),p=o.n(d),s=o(19624),l=o.n(s),m=o(96226),b=o.n(m),u=(o(77675),o(19365),o(51107));const C={id:"create-deletion-attempt-for-connector-id-manage-admin-deletion-attempt-post",title:"Create Deletion Attempt For Connector Id",description:"Create Deletion Attempt For Connector Id",sidebar_label:"Create Deletion Attempt For Connector Id",hide_title:!0,hide_table_of_contents:!0,api:"eJyVVU1vGjEQ/SurOW/CNu1pb2mSqiitggLtBa3Q4B3AwWtvbG8ShPa/V2Mv30FpLmDs+XzvzbAGU5NFL43ul5CDsISeJiUp4rsJek9V7SczYyfCaE3CGzuR5aRCjXOaYFlJfWpeG+chBUvPDTn/3ZQryNcgjPakPR+xrpUUIW/vyRnNd04sqEI+1Zar8pJc57bNy7/9qibIQWpPc7KQgpde8c3NxjDpl9Cm3ExJ2ktUH3puLYNrm25MzfSJxKYVaamEfHxY0HGa4p16duEHKG0/nGeSLLScahfa24bChauNdrH7qyzjr5KcsLJmwCCHYSMEOTdrVPLYGXMh/4lvG9J+u7o6DfwXlSyDW3JnrbGfiHrEWkkepeKT9FS5UwNlxMEr6tXDDPLxlibnrdRzaNMT4tpixxBai6s9Kn+ZWCALoHLzPdq7eDvT3+Qczgm2wc6bBjCSEb9+pA7uK6bu7PYUsYM3onu+jdsI33vJNiY/R6PBScDIrSPRWOlXAc7rQf+eVjfGLCVBPi7aIj1i/SZMfXLbjXFyHcc4+WFscjBUKVTkF4Y3RTfiNfoF5NCL+6AX9kFvsw8uun0AXJF9IetCQY1VkMPC+zrv9ZQRqBbG+fxrlmXAxW2qH7K0olgOe9jyhLW8J4ZNchsiPqegseLXGTqPtWwcWYeNXwQ0WbePu71094ZVreh0z2Qn+yNrOc/MhPwdB8PgnXxHsSTN+HCTEdTsMrv8wgwzUhWGYekK+wTeB0Rt+/b05nu1QhlkHvBcd1SMIVIBKQQyQowjOooUGHE2Xq+n6OiPVW3L188NWVZNkcILWolTFSWTwoKwJBv4W9IqbjfeCxdhKNhcNZGSox3B8xs9roWgIIbztsWewgYPwxGkMO3+PSpTso/FVx44fIUcIAUToAkaCXdrUKjnDQOQQ4zJrAf6D3SzDLrpDntbB/Vqr8ITCaVdL/y5t5kOvdbrKMy23drHp7MeHboba+a1aNv2H16Qo34=",sidebar_class_name:"post api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},h=void 0,f={},y=[];function N(e){const t={p:"p",...(0,i.R)(),...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsx)(u.default,{as:"h1",className:"openapi__heading",children:"Create Deletion Attempt For Connector Id"}),"\n",(0,n.jsx)(c(),{method:"post",path:"/manage/admin/deletion-attempt",context:"endpoint"}),"\n",(0,n.jsx)(t.p,{children:"Create Deletion Attempt For Connector Id"}),"\n",(0,n.jsx)(u.default,{id:"request",as:"h2",className:"openapi-tabs__heading",children:"Request"}),"\n",(0,n.jsx)(p(),{parameters:void 0}),"\n",(0,n.jsx)(l(),{title:"Body",body:{content:{"application/json":{schema:{properties:{connector_id:{type:"integer",title:"Connector Id"},credential_id:{type:"integer",title:"Credential Id"}},type:"object",required:["connector_id","credential_id"],title:"ConnectorCredentialPairIdentifier"}}},required:!0}}),"\n",(0,n.jsx)(b(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{}}}},422:{description:"Validation Error",content:{"application/json":{schema:{properties:{detail:{items:{properties:{loc:{items:{anyOf:[{type:"string"},{type:"integer"}]},type:"array",title:"Location"},msg:{type:"string",title:"Message"},type:{type:"string",title:"Error Type"}},type:"object",required:["loc","msg","type"],title:"ValidationError"},type:"array",title:"Detail"}},type:"object",title:"HTTPValidationError"}}}}}})]})}function g(e={}){const{wrapper:t}={...(0,i.R)(),...e.components};return t?(0,n.jsx)(t,{...e,children:(0,n.jsx)(N,{...e})}):N(e)}}}]);