const tabBoxEl=document.querySelectorAll(".option-wrap .tab-box"),btnLink=document.querySelectorAll(".nav-tabs .nav-link");btnLink.forEach(t=>{t.addEventListener("click",function(){window.scroll({top:0,behavior:"smooth"})})}),tabBoxEl.forEach(function(t){t.addEventListener("click",function(){let t=this.getAttribute("data-class");btnLink.forEach(function(e){let o=e.getAttribute("aria-controls");o===t&&e.click()})})});const productElementTab=document.querySelectorAll("[data-productDetail='product-detail']"),tabElement=document.querySelectorAll(".tab-pane"),orderSidebarlink=document.querySelector("#orders-tab"),tabRemoveClassFunction=function(t){t.forEach(t=>{t.classList.remove("show","active")})};productElementTab.forEach(t=>{t.addEventListener("click",function(){tabRemoveClassFunction(tabElement);let t=document.querySelector("#orders-details");t.classList.add("show","active")})}),orderSidebarlink.addEventListener("click",function(){tabRemoveClassFunction(tabElement);let t=document.querySelector("#orders");t.classList.add("show","active")});