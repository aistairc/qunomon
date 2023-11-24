import pageMixin from "./pageMixin";
import subMenuClose from "@/assets/google_icon_menu.svg";
import subMenuOpen from "@/assets/google_icon_menu_open.svg";

export const subMenuMixin = {
    data(){
        return {            
            icon1: subMenuClose,
            icon2: subMenuOpen,
            isActive: this.setIsActive()
        }
    },
    methods: {
        setIsActive(){
            let checkIsActive = sessionStorage.getItem('isActive')

            if (checkIsActive === null){
                this.updateIsActive(false);
                return false;
            }else{
                if (checkIsActive === "false"){
                    this.updateIsActive(false);
                    return false;
                }else{
                    this.updateIsActive(true);
                    return true;
                }
            }
        },
        updateIsActive(checkIsActive){
            pageMixin.$emit('classToggled', checkIsActive);
        },
        toggleSubmenu(isActive) {
            this.isActive= !isActive;
            sessionStorage.setItem('isActive', (!isActive).toString());
            pageMixin.$emit('classToggled', !isActive);
        }
    }
}