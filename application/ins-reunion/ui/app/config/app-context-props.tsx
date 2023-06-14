import CoreUIContextProps from "@bl/core-ui/bl/core-ui/config/core-ui-context-props";
import {_t} from "@pfo/pf-pweb-i18n/app/pweb-i18n";
import AuthenticationService from "bl-identity-acl/app/service/authentication-service";
import {PFUtil} from "@pfo/pf-react/src/artifacts/utils/pf-util";


export default class AppContextProps extends CoreUIContextProps {

    loginName: string = _t("Ins Reunion")
    orgName: string = _t("Ins Reunion")

    logout: any = () => {
        AuthenticationService.instance().logout()
        PFUtil.redirectTo("/")
    }

    profile: any = () => {
        PFUtil.redirectTo("/my-profile")
    }

}