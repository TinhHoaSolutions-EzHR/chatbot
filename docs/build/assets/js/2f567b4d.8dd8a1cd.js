"use strict";(self.webpackChunkdocss=self.webpackChunkdocss||[]).push([[5321],{80119:(t,e,o)=>{o.r(e),o.d(e,{assets:()=>M,contentTitle:()=>g,default:()=>f,frontMatter:()=>h,metadata:()=>s,toc:()=>y});const s=JSON.parse('{"id":"chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get","title":"Get Most Boosted Docs","description":"Get Most Boosted Docs","source":"@site/docs/chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get.api.mdx","sourceDirName":"chatbot-api","slug":"/chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get","permalink":"/docs/chatbot-api/get-most-boosted-docs-manage-admin-doc-boosts-get","draft":false,"unlisted":false,"editUrl":null,"tags":[],"version":"current","frontMatter":{"id":"get-most-boosted-docs-manage-admin-doc-boosts-get","title":"Get Most Boosted Docs","description":"Get Most Boosted Docs","sidebar_label":"Get Most Boosted Docs","hide_title":true,"hide_table_of_contents":true,"api":"eJy1VU1v2zgQ/SvCnFpAW7vZPemWNEUbNMEWTdqLYRg0NbZYU6RKjooVBP33xZCSLMWxu3voxbI4328en1qwFTpBypq7HDLYI21K62mztdYT5pvcSr8phRF73Ii8VIZPotVv9kiQQiWcKJHQechWLTj8USuHOWTkakzBywJLAVkL1FQIGWyt1SgMpECKNJ9ce4kmV2YPXQpGlHwmxrMUlIEMftToGujS/1BBGcI9ukmFe1UqmmTX4X2eeZ2CQ19Z49Fzsqvlkh85eulUxRBBBo+1lOj9rtbJl94ZUpDWEBpid1FVWsmA6OK755h20qAiLEPyyjHwpGKp3Mq6REMblU/G8OTi/MMUt71bcpfzLB5LYUjJX0Q99m59lFbmcMn9nu1dCmHHF0G9CR5dCoXKczQXV/wxunRdOvjY7XeUvIPjOlczIOYD9o0PfY1F18/6ubUSjkWEc6KZtDHsLPmAlDxYT8lNJHpya6VPHgLRk2smOp9Eq2dv6Dpu/q+rq1NSfBNa5WHlyXvnrPs/jHhGBCSh9AWmaCtnVmGav3fh3s33yffk2eK69Xlc7m1skKEr/f4SPx7Qe7HHI8jnXQMYyRNbf7V4niuW7v0mez3CG9E9P8ZthO+lYiMRn54+nySMu/Uoa6eoCXBef777hM07aw8KIVutWR7mW3+RQjwEUmF7MQ3ySAVksIgiuggiusit/COKaKC5+zmoZ+00ZFAQVdlioa0UurCesj+Xy2VQqKHHRyZQpMS803EbolKfsBk0TkbzKIA74UlUqvbovKipCJgps7Mhw6Acoqw0JjdCHtDwFeQ24/DLN8s3b3kTlfVUikDqPvU5XGbojW0S/kOLSgsVuBfGb3vMVhAxgxQCapzjiNs6hSIo1Aradis8fnW66/g46jmjmSsvtpoZthPa40kP4y2FV196Mr5OIH25twM2z75LP4Wu2S/ctt9Qa/hKHeus+cUpLhRImUKBIkcXpo1B11JiNY060R/OMpL0w/snxpcpMOPOIXCn/zPRF2GaSe4TGg2t8+9Eg+ZRbRvJ2XWjfzSdjeinHLwZpHXXdf8CcL74pw==","sidebar_class_name":"get api-method","info_path":"docs/chatbot-api/sample-backend","custom_edit_url":null},"sidebar":"chatbotApiSidebar","previous":{"title":"Admin Search","permalink":"/docs/chatbot-api/admin-search-admin-search-post"},"next":{"title":"Document Boost Update","permalink":"/docs/chatbot-api/document-boost-update-manage-admin-doc-boosts-post"}}');var i=o(74848),a=o(28453),n=o(57742),d=o.n(n),c=o(78178),p=o.n(c),l=o(19624),r=o.n(l),m=o(96226),b=o.n(m),u=(o(77675),o(19365),o(51107));const h={id:"get-most-boosted-docs-manage-admin-doc-boosts-get",title:"Get Most Boosted Docs",description:"Get Most Boosted Docs",sidebar_label:"Get Most Boosted Docs",hide_title:!0,hide_table_of_contents:!0,api:"eJy1VU1v2zgQ/SvCnFpAW7vZPemWNEUbNMEWTdqLYRg0NbZYU6RKjooVBP33xZCSLMWxu3voxbI4328en1qwFTpBypq7HDLYI21K62mztdYT5pvcSr8phRF73Ii8VIZPotVv9kiQQiWcKJHQechWLTj8USuHOWTkakzBywJLAVkL1FQIGWyt1SgMpECKNJ9ce4kmV2YPXQpGlHwmxrMUlIEMftToGujS/1BBGcI9ukmFe1UqmmTX4X2eeZ2CQ19Z49Fzsqvlkh85eulUxRBBBo+1lOj9rtbJl94ZUpDWEBpid1FVWsmA6OK755h20qAiLEPyyjHwpGKp3Mq6REMblU/G8OTi/MMUt71bcpfzLB5LYUjJX0Q99m59lFbmcMn9nu1dCmHHF0G9CR5dCoXKczQXV/wxunRdOvjY7XeUvIPjOlczIOYD9o0PfY1F18/6ubUSjkWEc6KZtDHsLPmAlDxYT8lNJHpya6VPHgLRk2smOp9Eq2dv6Dpu/q+rq1NSfBNa5WHlyXvnrPs/jHhGBCSh9AWmaCtnVmGav3fh3s33yffk2eK69Xlc7m1skKEr/f4SPx7Qe7HHI8jnXQMYyRNbf7V4niuW7v0mez3CG9E9P8ZthO+lYiMRn54+nySMu/Uoa6eoCXBef777hM07aw8KIVutWR7mW3+RQjwEUmF7MQ3ySAVksIgiuggiusit/COKaKC5+zmoZ+00ZFAQVdlioa0UurCesj+Xy2VQqKHHRyZQpMS803EbolKfsBk0TkbzKIA74UlUqvbovKipCJgps7Mhw6Acoqw0JjdCHtDwFeQ24/DLN8s3b3kTlfVUikDqPvU5XGbojW0S/kOLSgsVuBfGb3vMVhAxgxQCapzjiNs6hSIo1Aradis8fnW66/g46jmjmSsvtpoZthPa40kP4y2FV196Mr5OIH25twM2z75LP4Wu2S/ctt9Qa/hKHeus+cUpLhRImUKBIkcXpo1B11JiNY060R/OMpL0w/snxpcpMOPOIXCn/zPRF2GaSe4TGg2t8+9Eg+ZRbRvJ2XWjfzSdjeinHLwZpHXXdf8CcL74pw==",sidebar_class_name:"get api-method",info_path:"docs/chatbot-api/sample-backend",custom_edit_url:null},g=void 0,M={},y=[];function j(t){const e={p:"p",...(0,a.R)(),...t.components};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(u.default,{as:"h1",className:"openapi__heading",children:"Get Most Boosted Docs"}),"\n",(0,i.jsx)(d(),{method:"get",path:"/manage/admin/doc-boosts",context:"endpoint"}),"\n",(0,i.jsx)(e.p,{children:"Get Most Boosted Docs"}),"\n",(0,i.jsx)(u.default,{id:"request",as:"h2",className:"openapi-tabs__heading",children:"Request"}),"\n",(0,i.jsx)(p(),{parameters:[{required:!0,schema:{type:"boolean",title:"Ascending"},name:"ascending",in:"query"},{required:!0,schema:{type:"integer",title:"Limit"},name:"limit",in:"query"}]}),"\n",(0,i.jsx)(r(),{title:"Body",body:void 0}),"\n",(0,i.jsx)(b(),{id:void 0,label:void 0,responses:{200:{description:"Successful Response",content:{"application/json":{schema:{items:{properties:{document_id:{type:"string",title:"Document Id"},semantic_id:{type:"string",title:"Semantic Id"},link:{type:"string",title:"Link"},boost:{type:"integer",title:"Boost"},hidden:{type:"boolean",title:"Hidden"}},type:"object",required:["document_id","semantic_id","link","boost","hidden"],title:"BoostDoc"},type:"array",title:"Response Get Most Boosted Docs Manage Admin Doc Boosts Get"}}}},422:{description:"Validation Error",content:{"application/json":{schema:{properties:{detail:{items:{properties:{loc:{items:{anyOf:[{type:"string"},{type:"integer"}]},type:"array",title:"Location"},msg:{type:"string",title:"Message"},type:{type:"string",title:"Error Type"}},type:"object",required:["loc","msg","type"],title:"ValidationError"},type:"array",title:"Detail"}},type:"object",title:"HTTPValidationError"}}}}}})]})}function f(t={}){const{wrapper:e}={...(0,a.R)(),...t.components};return e?(0,i.jsx)(e,{...t,children:(0,i.jsx)(j,{...t})}):j(t)}}}]);