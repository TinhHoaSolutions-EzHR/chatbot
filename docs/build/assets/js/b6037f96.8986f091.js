"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[4958],{48024:(e,s,t)=>{t.r(s),t.d(s,{assets:()=>y,contentTitle:()=>m,default:()=>j,frontMatter:()=>g,metadata:()=>i,toc:()=>x});const i=JSON.parse('{"id":"chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get","title":"Get User Chat Sessions","description":"Get User Chat Sessions","source":"@site/docs/chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get","permalink":"/docs/chatbot-api/get-user-chat-sessions-chat-get-user-chat-sessions-get","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"get-user-chat-sessions-chat-get-user-chat-sessions-get","title":"Get User Chat Sessions","description":"Get User Chat Sessions","sidebar_label":"Get User Chat Sessions","hide_title":true,"hide_table_of_contents":true,"api":"eJyFk0Fv2zAMhf+KwbPaeNvNt64biqLAUCztKQgCVWFiNbakinSwwPB/H2jZbpIuaw6ObD09Pn+kW/ABo2br3f0aCtgirxrCuDKl5hUhkfWO0t2FvS0yKIhIwTtCgqKFr3kuf2skE20Qcyhg3hiDRJumyn4PYlBgvGN0LHIdQmVNn2X2SnKmBTIl1lpWIUpStqnCWF3WlrGmjxK7lisfAkIB1jFuMYICtlzJk/s1dAqcrvFIRhyt2x6pfsl+pyBgJO/06hPTxyTLkjnbGlcmomZc/6/Ik60xux10nRxMQv/yiibBfWtsFJOFvNYQ+yTVWbXlu/ttqXmecP1A1rYieC+hY9SHoyjzketnMaYG/LsSTS3u5KeA0DTR8gGKRQs3j/cPeLj1fmcRisWyW6qzYblDzp4JYyae2ZRKQY1c+mFShYDmEgqYyUjOtshXMqBXcndF74cI4x4j9bWbWEEBJXMoZrPKG12Vnrj4luc5SI4x6FwmL03SadypjzrYBxR4VhKbtD2OFGw0sQ5W8pBuuOyJWrfxvcOIW9ehwuy7Njt00kSJmQjk1/n1l370PHGt+69hsL4I54ThlJPxD89Cpa0Tu/792wHcAgQVKLiAbqlA6IiwbV804XOsuk4evzUYpZlLBXsdrX6pUicVlKjXGHvWOzxAATfGYJAie101CdzZhy7cp8be/XwCBT2yE9a7nvWwEPdxyx2OvD9gV0MKuXbqwqm2Tc3sukmfti6eGN5yVAvbZdd1fwE/y9KR","sidebar_class_name":"get api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Auth:Database.Logout","permalink":"/docs/chatbot-api/auth-database-logout-auth-logout-post"},"next":{"title":"Get Chat Session","permalink":"/docs/chatbot-api/get-chat-session-chat-get-chat-session-session-id-get"}}');var a=t(74848),n=t(28453),o=t(57742),c=t.n(o),r=t(78178),h=t.n(r),l=t(19624),p=t.n(l),d=t(96226),u=t.n(d),b=(t(77675),t(19365),t(51107));const g={id:"get-user-chat-sessions-chat-get-user-chat-sessions-get",title:"Get User Chat Sessions",description:"Get User Chat Sessions",sidebar_label:"Get User Chat Sessions",hide_title:!0,hide_table_of_contents:!0,api:"eJyFk0Fv2zAMhf+KwbPaeNvNt64biqLAUCztKQgCVWFiNbakinSwwPB/H2jZbpIuaw6ObD09Pn+kW/ABo2br3f0aCtgirxrCuDKl5hUhkfWO0t2FvS0yKIhIwTtCgqKFr3kuf2skE20Qcyhg3hiDRJumyn4PYlBgvGN0LHIdQmVNn2X2SnKmBTIl1lpWIUpStqnCWF3WlrGmjxK7lisfAkIB1jFuMYICtlzJk/s1dAqcrvFIRhyt2x6pfsl+pyBgJO/06hPTxyTLkjnbGlcmomZc/6/Ik60xux10nRxMQv/yiibBfWtsFJOFvNYQ+yTVWbXlu/ttqXmecP1A1rYieC+hY9SHoyjzketnMaYG/LsSTS3u5KeA0DTR8gGKRQs3j/cPeLj1fmcRisWyW6qzYblDzp4JYyae2ZRKQY1c+mFShYDmEgqYyUjOtshXMqBXcndF74cI4x4j9bWbWEEBJXMoZrPKG12Vnrj4luc5SI4x6FwmL03SadypjzrYBxR4VhKbtD2OFGw0sQ5W8pBuuOyJWrfxvcOIW9ehwuy7Njt00kSJmQjk1/n1l370PHGt+69hsL4I54ThlJPxD89Cpa0Tu/792wHcAgQVKLiAbqlA6IiwbV804XOsuk4evzUYpZlLBXsdrX6pUicVlKjXGHvWOzxAATfGYJAie101CdzZhy7cp8be/XwCBT2yE9a7nvWwEPdxyx2OvD9gV0MKuXbqwqm2Tc3sukmfti6eGN5yVAvbZdd1fwE/y9KR",sidebar_class_name:"get api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},m=void 0,y={},x=[];function f(e){const s={p:"p",...(0,n.R)(),...e.components};return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(b.default,{as:"h1",className:"openapi__heading",children:"Get User Chat Sessions"}),"\n",(0,a.jsx)(c(),{method:"get",path:"/chat/get-user-chat-sessions",context:"endpoint"}),"\n",(0,a.jsx)(s.p,{children:"Get User Chat Sessions"}),"\n",(0,a.jsx)(h(),{parameters:void 0}),"\n",(0,a.jsx)(p(),{title:"Body",body:void 0}),"\n",(0,a.jsx)(u(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{properties:{sessions:{items:{properties:{id:{type:"integer",title:"Id"},name:{type:"string",title:"Name"},persona_id:{type:"integer",title:"Persona Id"},time_created:{type:"string",title:"Time Created"}},type:"object",required:["id","name","persona_id","time_created"],title:"ChatSessionDetails"},type:"array",title:"Sessions"}},type:"object",required:["sessions"],title:"ChatSessionsResponse"}}}}}})]})}function j(e={}){const{wrapper:s}={...(0,n.R)(),...e.components};return s?(0,a.jsx)(s,{...e,children:(0,a.jsx)(f,{...e})}):f(e)}}}]);