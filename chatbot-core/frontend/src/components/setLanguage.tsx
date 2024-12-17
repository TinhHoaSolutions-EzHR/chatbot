import React from 'react'
import setLanguage from 'next-translate/setLanguage'

export default function ChangeLanguage({
    lang,
                                       }: {
    lang: string;
}) {
    return (
        <button onClick={async () => await setLanguage(lang)}>EN</button>
    )
}