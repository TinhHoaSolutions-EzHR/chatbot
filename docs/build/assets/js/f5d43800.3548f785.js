"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[4757],{674:(e,t,a)=>{a.r(t),a.d(t,{assets:()=>b,contentTitle:()=>h,default:()=>G,frontMatter:()=>y,metadata:()=>s,toc:()=>f});const s=JSON.parse('{"id":"chatbot-api/get-tags-query-valid-tags-get","title":"Get Tags","description":"Get Tags","source":"@site/docs/chatbot-api/get-tags-query-valid-tags-get.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/get-tags-query-valid-tags-get","permalink":"/docs/chatbot-api/get-tags-query-valid-tags-get","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"get-tags-query-valid-tags-get","title":"Get Tags","description":"Get Tags","sidebar_label":"Get Tags","hide_title":true,"hide_table_of_contents":true,"api":"eJydVUtvGzcQ/ivCnFlLdYoe9uYmQRK4RY1azcUQhBF3dpcWl2T4cKIK+9+LIVfSKraSICetON+8vnntwTryGJU1H2qooKW4jtiG9adEfrd+Qq3q8tBSBAEOPfYUyQeoHvbg6VNSnmqoGtSBBATZUY9Q7SHuHEEFIXplWhAQVdT88BdG2c3uMEbyBgYBBnt+7/l97cZ3AcpABTkKGMSPeNpYqwnNxNWN1vbz7M5To76AgJoaTDpCFX2ik2Nk1NodUFO/KwGegrMmUGBP14sF/9QUpFeOSYMK7pOUFEKT9OyfEQwCpDWRTGQ4OqeVzBzPHwPr7CfRO88ViKp4YKr5V0Xqw4vi9ZZ23+J3ie3slpi0jH5Cneh7+I8ZNAgINnn5IpxM6qF6AGVaCpzKGp0CAUGj3IKAz7QBAa21raZ17dUTk9D2qDSIXDwKMXqUW/IsULFLm/KhMX8kn0BwEbchFpPSmkYnMpJN1SpIm3zmNhSVgJpCY32WPyqP3J/e1knGjUVfg4BGaRYam2sl4L+klQMBWhlCDqRLm+Asd3ZtZerJxFe/L3IiOesxn6AiBVYnU1Pg2LS1TlkOokNPzirDNiJhz7jGU+gycnUi+s3o4L5wLL5qoxszY47HYbyCgQtYimA3jyTjyGMZgodjK0zLfCzgxG1xt8QWTgbRe9yd90D4EYdhaniJ7bHfh4G1f7u+fj4eH3mF5Jxmb723/udno6bI7XR5OrSVZ1I0u7+bvKfOu5n3yfiiTKSWPAyry+z8aUuATGAf2m8uNwoBWzpRfRmayZgtWfo95jmv4nrETapworewezmNN4W+l5wdIO+Xy7tnBkttA8nkVdxlOm/uPtzS7rW1W0VQPax4UZ5X/R3FWe4qAT3Fzo63JV+Q2EEF87xi5/nA/BILMpB/OlyW5DVU0MXoqvlcW4m6syFWrxaLRd7Lh3juuVlK+c+jOjKPTt3mOcmbXRbxcfs3GCI6lQL5gCl2mR9lGpstHGYIe6dp9gevL8N7hcMsiS6uFle/MuvOhthjbuDR9ISDM3KOkUX6EudOo8qtlTPej/w8jCdIwIShlQAmgaX7/QYD/ev1MPBzATNvtQq40ZM7mc/Fs+s6ngXIs3BB56vDeFJZ8R+vWCdXX0BHWJPPARTdGynJxYnWs0FnK8fWePd2CQIy/2eFKwtu/JgMMprdxPazGh4y2NJuOuznWvt96YxhOOKfxjt4QWPM8oDmsq2GYfgfInonaw==","sidebar_class_name":"get api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Get Max Document Tokens","permalink":"/docs/chatbot-api/get-max-document-tokens-chat-max-selected-document-tokens-get"},"next":{"title":"Get Search Type","permalink":"/docs/chatbot-api/get-search-type-query-search-intent-post"}}');var i=a(74848),n=a(28453),o=a(57742),r=a.n(o),l=a(78178),p=a.n(l),d=a(19624),c=a.n(d),g=a(96226),u=a.n(g),m=(a(77675),a(19365),a(51107));const y={id:"get-tags-query-valid-tags-get",title:"Get Tags",description:"Get Tags",sidebar_label:"Get Tags",hide_title:!0,hide_table_of_contents:!0,api:"eJydVUtvGzcQ/ivCnFlLdYoe9uYmQRK4RY1azcUQhBF3dpcWl2T4cKIK+9+LIVfSKraSICetON+8vnntwTryGJU1H2qooKW4jtiG9adEfrd+Qq3q8tBSBAEOPfYUyQeoHvbg6VNSnmqoGtSBBATZUY9Q7SHuHEEFIXplWhAQVdT88BdG2c3uMEbyBgYBBnt+7/l97cZ3AcpABTkKGMSPeNpYqwnNxNWN1vbz7M5To76AgJoaTDpCFX2ik2Nk1NodUFO/KwGegrMmUGBP14sF/9QUpFeOSYMK7pOUFEKT9OyfEQwCpDWRTGQ4OqeVzBzPHwPr7CfRO88ViKp4YKr5V0Xqw4vi9ZZ23+J3ie3slpi0jH5Cneh7+I8ZNAgINnn5IpxM6qF6AGVaCpzKGp0CAUGj3IKAz7QBAa21raZ17dUTk9D2qDSIXDwKMXqUW/IsULFLm/KhMX8kn0BwEbchFpPSmkYnMpJN1SpIm3zmNhSVgJpCY32WPyqP3J/e1knGjUVfg4BGaRYam2sl4L+klQMBWhlCDqRLm+Asd3ZtZerJxFe/L3IiOesxn6AiBVYnU1Pg2LS1TlkOokNPzirDNiJhz7jGU+gycnUi+s3o4L5wLL5qoxszY47HYbyCgQtYimA3jyTjyGMZgodjK0zLfCzgxG1xt8QWTgbRe9yd90D4EYdhaniJ7bHfh4G1f7u+fj4eH3mF5Jxmb723/udno6bI7XR5OrSVZ1I0u7+bvKfOu5n3yfiiTKSWPAyry+z8aUuATGAf2m8uNwoBWzpRfRmayZgtWfo95jmv4nrETapworewezmNN4W+l5wdIO+Xy7tnBkttA8nkVdxlOm/uPtzS7rW1W0VQPax4UZ5X/R3FWe4qAT3Fzo63JV+Q2EEF87xi5/nA/BILMpB/OlyW5DVU0MXoqvlcW4m6syFWrxaLRd7Lh3juuVlK+c+jOjKPTt3mOcmbXRbxcfs3GCI6lQL5gCl2mR9lGpstHGYIe6dp9gevL8N7hcMsiS6uFle/MuvOhthjbuDR9ISDM3KOkUX6EudOo8qtlTPej/w8jCdIwIShlQAmgaX7/QYD/ev1MPBzATNvtQq40ZM7mc/Fs+s6ngXIs3BB56vDeFJZ8R+vWCdXX0BHWJPPARTdGynJxYnWs0FnK8fWePd2CQIy/2eFKwtu/JgMMprdxPazGh4y2NJuOuznWvt96YxhOOKfxjt4QWPM8oDmsq2GYfgfInonaw==",sidebar_class_name:"get api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},h=void 0,b={},f=[];function T(e){const t={p:"p",...(0,n.R)(),...e.components};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(m.default,{as:"h1",className:"openapi__heading",children:"Get Tags"}),"\n",(0,i.jsx)(r(),{method:"get",path:"/query/valid-tags",context:"endpoint"}),"\n",(0,i.jsx)(t.p,{children:"Get Tags"}),"\n",(0,i.jsx)(m.default,{id:"request",as:"h2",className:"openapi-tabs__heading",children:"Request"}),"\n",(0,i.jsx)(p(),{parameters:[{required:!1,schema:{type:"string",title:"Match Pattern"},name:"match_pattern",in:"query"},{required:!1,schema:{type:"boolean",title:"Allow Prefix",default:!0},name:"allow_prefix",in:"query"}]}),"\n",(0,i.jsx)(c(),{title:"Body",body:void 0}),"\n",(0,i.jsx)(u(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{properties:{tags:{items:{properties:{tag_key:{type:"string",title:"Tag Key"},tag_value:{type:"string",title:"Tag Value"},source:{type:"string",enum:["ingestion_api","slack","web","google_drive","gmail","requesttracker","github","gitlab","guru","bookstack","confluence","discourse","slab","salesforce","jira","productboard","file","notion","zulip","linear","hubspot","document360","gong","google_sites","zendesk","loopio","sharepoint","teams","freshdesk"],title:"DocumentSource",description:"An enumeration."}},type:"object",required:["tag_key","tag_value","source"],title:"SourceTag"},type:"array",title:"Tags"}},type:"object",required:["tags"],title:"TagResponse"}}}},422:{description:"Validation Error",content:{"application/json":{schema:{properties:{detail:{items:{properties:{loc:{items:{anyOf:[{type:"string"},{type:"integer"}]},type:"array",title:"Location"},msg:{type:"string",title:"Message"},type:{type:"string",title:"Error Type"}},type:"object",required:["loc","msg","type"],title:"ValidationError"},type:"array",title:"Detail"}},type:"object",title:"HTTPValidationError"}}}}}})]})}function G(e={}){const{wrapper:t}={...(0,n.R)(),...e.components};return t?(0,i.jsx)(t,{...e,children:(0,i.jsx)(T,{...e})}):T(e)}}}]);