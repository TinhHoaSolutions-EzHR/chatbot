"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[8472],{75906:(t,e,s)=>{s.r(e),s.d(e,{assets:()=>D,contentTitle:()=>h,default:()=>J,frontMatter:()=>g,metadata:()=>i,toc:()=>j});const i=JSON.parse('{"id":"chatbot-api/list-prompts-prompt-get","title":"List Prompts","description":"List Prompts","source":"@site/docs/chatbot-api/list-prompts-prompt-get.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/list-prompts-prompt-get","permalink":"/docs/chatbot-api/list-prompts-prompt-get","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"list-prompts-prompt-get","title":"List Prompts","description":"List Prompts","sidebar_label":"List Prompts","hide_title":true,"hide_table_of_contents":true,"api":"eJyNVE1v2zAM/SsBz0bjbTffunYogg5DsXSnIAgYhanVyJYq0d0Mw/99oOR4TtIWu9iG9Ei9D9EdWEceWdt6sYMCjA68cd5WjsPw3jwRQwaegrN1oABFB5/zXF47CsprJ9VQwLJRikLYN2b2cwBDBsrWTDULHJ0zWsXD5s9BajoIqqQK5UszVbG588KJdTpK7+TJrSMoQNdMT+QhA9ZsZGWxgz6DGiuawAJ7XT9NUD9kv88glOhp2nBrrSGsJ9BlgvTZqbr3e99OYHJEG5iqwbuP6pYROHtIwD4DxnD4j7pHDIdJla6VaXa0UZqjs+FDdYuEnt2MaBGKTKwr2uBv9PRh/e0AnV1HaHRpj43hS+JvFCfoSF40J6zdPpNKt+yl0TGilSQ/JDsGdxrKudmnFr5lzYXWC/7rf3QTzWWNLpQ2JZTYovfYTnQdb/vsuw5HdWF4z+5IlPYiNpBqvOYWilUH1w+Le2pvrD1ogmK17tdnNw6m3SCDiri0MqNpHh1yCQXMR7WB/Cv5EJs33kABJbMr5nNjFZrSBi6+5HkOctCRyVKmL83ZKZ8xRXT6ntpoJhSg0vZx4GCPgdHpJpAP2HAZM9X13sYOx4uOlTM0+4rqQLVkKDSTxPwqv/okzjobuMI4Z0PrM/VvDyPTH547gzqOXlTdDc6s4F+iIl5Wum6LgX550/ey/NKQlzDWGbyi17g1KYkMSsId+WjlgVoo4Fopii6/ommSL2f/MrF1jOju2yNkEB05sfIQrRw+pPtxq24nvS9czQYW8uyzd6q6LmXV9yM+bb1bMag8osXEdd/3fwFVjRcR","sidebar_class_name":"get api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Get Default Model","permalink":"/docs/chatbot-api/get-default-model-admin-persona-utils-default-model-get"},"next":{"title":"Create Prompt","permalink":"/docs/chatbot-api/create-prompt-prompt-post"}}');var o=s(74848),p=s(28453),r=s(57742),a=s.n(r),n=s(78178),d=s.n(n),l=s(19624),m=s.n(l),c=s(96226),u=s.n(c),b=(s(77675),s(19365),s(51107));const g={id:"list-prompts-prompt-get",title:"List Prompts",description:"List Prompts",sidebar_label:"List Prompts",hide_title:!0,hide_table_of_contents:!0,api:"eJyNVE1v2zAM/SsBz0bjbTffunYogg5DsXSnIAgYhanVyJYq0d0Mw/99oOR4TtIWu9iG9Ei9D9EdWEceWdt6sYMCjA68cd5WjsPw3jwRQwaegrN1oABFB5/zXF47CsprJ9VQwLJRikLYN2b2cwBDBsrWTDULHJ0zWsXD5s9BajoIqqQK5UszVbG588KJdTpK7+TJrSMoQNdMT+QhA9ZsZGWxgz6DGiuawAJ7XT9NUD9kv88glOhp2nBrrSGsJ9BlgvTZqbr3e99OYHJEG5iqwbuP6pYROHtIwD4DxnD4j7pHDIdJla6VaXa0UZqjs+FDdYuEnt2MaBGKTKwr2uBv9PRh/e0AnV1HaHRpj43hS+JvFCfoSF40J6zdPpNKt+yl0TGilSQ/JDsGdxrKudmnFr5lzYXWC/7rf3QTzWWNLpQ2JZTYovfYTnQdb/vsuw5HdWF4z+5IlPYiNpBqvOYWilUH1w+Le2pvrD1ogmK17tdnNw6m3SCDiri0MqNpHh1yCQXMR7WB/Cv5EJs33kABJbMr5nNjFZrSBi6+5HkOctCRyVKmL83ZKZ8xRXT6ntpoJhSg0vZx4GCPgdHpJpAP2HAZM9X13sYOx4uOlTM0+4rqQLVkKDSTxPwqv/okzjobuMI4Z0PrM/VvDyPTH547gzqOXlTdDc6s4F+iIl5Wum6LgX550/ey/NKQlzDWGbyi17g1KYkMSsId+WjlgVoo4Fopii6/ommSL2f/MrF1jOju2yNkEB05sfIQrRw+pPtxq24nvS9czQYW8uyzd6q6LmXV9yM+bb1bMag8osXEdd/3fwFVjRcR",sidebar_class_name:"get api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},h=void 0,D={},j=[];function y(t){const e={p:"p",...(0,p.R)(),...t.components};return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(b.default,{as:"h1",className:"openapi__heading",children:"List Prompts"}),"\n",(0,o.jsx)(a(),{method:"get",path:"/prompt",context:"endpoint"}),"\n",(0,o.jsx)(e.p,{children:"List Prompts"}),"\n",(0,o.jsx)(d(),{parameters:void 0}),"\n",(0,o.jsx)(m(),{title:"Body",body:void 0}),"\n",(0,o.jsx)(u(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{items:{properties:{id:{type:"integer",title:"Id"},name:{type:"string",title:"Name"},shared:{type:"boolean",title:"Shared"},description:{type:"string",title:"Description"},system_prompt:{type:"string",title:"System Prompt"},task_prompt:{type:"string",title:"Task Prompt"},include_citations:{type:"boolean",title:"Include Citations"},datetime_aware:{type:"boolean",title:"Datetime Aware"},default_prompt:{type:"boolean",title:"Default Prompt"}},type:"object",required:["id","name","shared","description","system_prompt","task_prompt","include_citations","datetime_aware","default_prompt"],title:"PromptSnapshot"},type:"array",title:"Response List Prompts Prompt Get"}}}}}})]})}function J(t={}){const{wrapper:e}={...(0,p.R)(),...t.components};return e?(0,o.jsx)(e,{...t,children:(0,o.jsx)(y,{...t})}):y(t)}}}]);